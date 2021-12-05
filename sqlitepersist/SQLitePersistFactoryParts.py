import sqlite3 as sq3
from sqlite3.dbapi2 import Error, OperationalError
import uuid
import datetime

from .SQLitePersistBasicClasses import *


class SQFactory():
    def __init__(self, name, dbfilename):
        self._name = name
        self._dbfilename = dbfilename
        self.__in_transaction = None
        sq3.register_adapter(uuid.UUID, SQFactory.adapt_uuid)
        sq3.register_converter("uuid", SQFactory.convert_uuid)
        self.conn = sq3.connect(dbfilename, detect_types=sq3.PARSE_DECLTYPES | sq3.PARSE_COLNAMES)
        self.conn.row_factory = sq3.Row
        self.lang = "GBR"

    def _gettablename(self, pinst):
        return pinst.__class__.__name__.lower()

    def try_createtable(self, pinst):
        try:
            self.createtable(pinst)
        except:
            pass

    def try_droptable(self, pinst):
        try:
            self.droptable(pinst)
        except:
            pass

    def createtable(self, pinst):
        pinstcls = pinst.__class__
        tablename = pinstcls.__name__.lower()
        memd = pinstcls._classdict[pinstcls]
        collst = "("
        first = True
        for key, val in memd.items():
            if first:
                collst += key + " " + self._get_dbtypename(val)
                first = False
            else:
                collst += "," + key + " " + self._get_dbtypename(val)

            if key == "_id": #id is always the primary key and nothing else
                collst += " PRIMARY KEY"

        collst += ")"

        cursor = self.conn.cursor()
        exs = "CREATE TABLE {0} {1}".format(tablename, collst)
        print(exs)
        cursor.execute(exs)

    def droptable(self, pinst):
        pinstcls = pinst.__class__
        tablename = pinstcls.__name__.lower()
        cursor = self.conn.cursor()
        exs = "DROP TABLE {0} ".format(tablename)
        print(exs)
        cursor.execute(exs)

    def _deleteinst(self, pinst):
        pass

    def delete(self, dco):
        """Delete the given persitent instance and do all the casscading deletes (if any). 
        Make sure that neither all the deletes du execute or none by using transactions behind the
        scenes"""
        curs = self.conn.cursor()
        try:
            curs.execute("BEGIN")
            try:
                self._notransdeletecascaded(curs, dco)
                curs.execute("COMMIT")
            except sq3.Error as err:
                curs.execute("ROLLBACK")
                raise Error(str(err))
        finally:
            curs.close()
        

    def _notransdeletecascaded(self, curs, dco):
        t = type(dco)

        if not issubclass(t, PBase):
            raise Exception("Type <{}> is not supported in MpFactory.delete()".format(t.__name__))

        if dco._id is None: raise BaseException("No delete withoud an _id!")

        membdict = dco._get_my_memberdict()
        for membkey, membval in membdict.items():
            decl = membval._declaration
            declt = type(decl)
            if issubclass(declt, JoinedEmbeddedObject) and decl.get_cascadedelete():
                self.resolve(dco, membkey)
                loco = getattr(dco, membkey)
                if not loco is None:
                    self._notransdeletecascaded(loco)

            elif issubclass(declt, JoinedEmbeddedList) and decl.get_cascadedelete():
                self.resolve(dco, membkey)
                locos = getattr(dco, membkey)
                for loco in locos:
                    self._notransdeletecascaded(loco)

        self._notransdelete(curs, dco)



    def _notransdelete(self, curs, dco):
        """Delete a data object from its collection 

            dco : The data object to be deleted (_id has to be filled!)
        """

        t = type(dco)

        if not issubclass(t, PBase):
            raise Exception("Type <{}> is not supported in MpFactory.delete()".format(t.__name__))

        if dco._id is None: raise BaseException("No delete withoud an _id!")
        
        delcls = type(dco)
        tablename = delcls._getclstablename()
        stmt = "DELETE FROM {0} WHERE _id='{1}'".format(tablename, str(dco._id))
        curs.execute(stmt)


    def _get_dbtypename(self, val):
        ot = val.get_outertype()
        if ot == None:
            return "NONE"
        else:
            return ot.name

       

    def flush(self, pinst : PBase):
        if pinst._id is None: #we need to insert
            pinst._id = uuid.uuid4()
            pinst.created = datetime.datetime.now()
            pinst.lastupdate = datetime.datetime.now()
            self._insert(pinst)
        else: #we need to update
            pinst.lastupdate = datetime.datetime.now()
            self._update(pinst)

        self.conn.commit()

    def _getvaluestuple(self, pinst):
        pinstcls = pinst.__class__
        memd = pinstcls._classdict[pinstcls]
        first = True
        valtuplst = []
        for key, val in memd.items():
            propvalue = pinst.__getattribute__(key)
            if propvalue is not None:
                valtuplst.append(propvalue)
                if first:
                    first = False
                    cquests = "?"
                    cnames = key
                else:
                    cquests += ", ?"
                    cnames += ", " + key
        return tuple(valtuplst), cnames, cquests

    def _insert(self, pinst : PBase):
        table = self._gettablename(pinst)
        curs = self.conn.cursor()
        valtuple, inscolnames, inscolquests = self._getvaluestuple(pinst)

        curs.execute("insert into " + table + "(" + inscolnames + ") values (" + inscolquests + ")", valtuple)

    def _update(self, pinst : PBase):
        pass

    def find(self, cls, findpar = None, orderlist=None, limit=None):
        """Find the data
        
        """
        if findpar is None: #do a select * eventually respecting limit
            return self._do_select(cls, findpar, orderlist, limit)
        elif type(findpar) is dict:
            return self._do_select(cls, findpar,  orderlist, limit)
        elif issubclass(type(findpar), BaseType):
            if findpar._id is None:
                raise Exception("SqFactory.find() with an Mpbase derived instance only works when this instance contains an _id")

            res = self.find_with_dict(cls, {"_id": findpar._id})
            return self._first_or_default(res)
        elif findpar is str:
            res = self.find_with_dict(cls, {"_id": findpar})
            return self._first_or_default(res)
        else:
            raise NotImplementedError("Unsupported type <{}> in findpar.".format(type(findpar)))

    def _do_select(self, cls, findpar, orderlist, limit):
        stmt = "SELECT * FROM {0}".format(cls._getclstablename())

        if findpar is not None:
            if len(findpar) > 0:
                stmt += " WHERE " + self._create_where(findpar)
                

        if limit is not None and limit >0:
            if findpar is None:
                stmt += " WHERE ROWNUM < " + str(limit)
            else:
                stmt += " AND ROWNUM<" + str(limit)

        if orderlist is not None:
            pass

        curs = self.conn.cursor()
        try:
            answ = curs.execute(stmt)
        except OperationalError as oe:
            print(stmt)
            raise Exception(stmt + " " + str(oe))
        return answ

    def _backmap(self, ops):
        mapping = {"$eq":"=", 
            "$neq":"<>",
            "$gt":">",
            "$lt":"<",
            "$gte":">=",
            "&lte":"<="}
        return mapping[ops]

    def _get_rightrightpart(self, val):
        t = type(val)
        if t is uuid.UUID or t is str:
            return "'" + str(val) + "'"

    def _ismulti(self, s):
        return s in ("$or", "$and")

    def _isbinary(self, s):
        return s in ("$lt", "$gt", "$eq", "$gte", "$lte")

    def _getbinarypart(self, op : str, operands : list):
        if len(operands) != 2:
            raise Exception("getbinraypart needs exactly two operands!")

        return "{0} {1} {2}".format(operands[0], self._backmap(op), self._get_rightrightpart(operands[1]))

    def _getoperand(self, operand):
        t = type(operand)
        if t is str:
            return "'{0}'".format(operand)
        elif t is int:
            return str(operand)
        elif t is float:
            return str(operand)
        elif t is uuid.UUID:
            return "'{0}'".format(operand)
        elif t is dict:
            return self._getoperanddict(operand)

    def _getoperanddict(self, operand):
        operandl = list(operand.items())
        op = operandl[0][0]
        right = operandl[0][1]
        tr = type(right)
        if self._ismulti(op):
            return "(....)"
        else:
            rightl = list(right.items())
            answ = "{0} {1} {2}".format(op, self._backmap(rightl[0][0]), self._getoperand(rightl[0][1]))
        
        return answ

    def _getmultipart(self, op: str, operands : list):
        first = True
        for operand in operands:
            if first:
                first = False
                answ = self._getoperand(operand)
            else:
                answ += " AND "
                answ += self._getoperand(operand)

        return answ

    def _create_where(self, findpar : dict):
        """creates the where part of the db-statement by evaluating the findpar dictionary"""
        answ = ""
        findparl = list(findpar.items())
        if len(findparl) > 1:
            raise Exception("findpar structure problem with top element")
        
        op = findparl[0][0]
        if not type(op) is str:
            raise Exception("no operator found in basic findpar dict")

        oplist = findparl[0][1]
        if not type(oplist) is list:
            raise Exception("first layer value must be a dictionary containing the operands")

        if self._ismulti(op):
            answ = self._getmultipart(op, oplist)            
        elif self._isbinary(op):
            answ = self._getbinarypart(op, oplist)

        return answ


    def _create_instance(self, cls : PBase, row):
        """create an instance of the object with a cursor to a selected row as cn
        """
        inst = cls()
        vd = inst._get_my_memberdict()

        for key, value in vd.items():
            if hasattr(inst, key) and getattr(inst, key) is not None:
                continue
            
            dbdta = row[key]
            decl = value._declaration
            setattr(inst, key, decl.to_innertype(dbdta))

        return inst

    @classmethod
    def adapt_uuid(cls, gid):
        return gid.hex

    @classmethod
    def convert_uuid(cls, text):
        if text.decode() == 'None':
            return None
        else:
            return uuid.UUID(hex=text.decode())




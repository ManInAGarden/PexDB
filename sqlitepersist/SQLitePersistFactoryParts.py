
from distutils.filelist import findall
from importlib.util import module_for_loader
import sqlite3 as sq3
from sqlite3.dbapi2 import Error, OperationalError
from typing import Type
import uuid
import datetime as dt

from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator

from .SQLitePersistBasicClasses import *
from .SQLitePPersistLogging import *


class SQFactory():
    
    unwritable = [JoinedEmbeddedList, JoinedEmbeddedObject]

    def __init__(self, name, dbfilename):
        self._name = name
        self._dbfilename = dbfilename
        sq3.register_adapter(uuid.UUID, SQFactory.adapt_uuid)
        sq3.register_converter("uuid", SQFactory.convert_uuid)
        self.conn = sq3.connect(dbfilename, detect_types=sq3.PARSE_DECLTYPES | sq3.PARSE_COLNAMES)
        self.conn.row_factory = sq3.Row
        self.lang = "GBR"
        self._catcache = {}
        self._logger = SQPLogger("./doesntmatter", DbgStmtLevel.NONE) #switch off debugging by default
        self._transafterdels = []
        self._intrans = False


    @property
    def InTransaction(self):
        return self._intrans

    def begin_transaction(self, loginfo : str = None):
        if self._intrans:
            raise Exception("A transaction has already benn started")

        self._transafterdels.clear()
        curs = self.conn.cursor()
        try:
            curs.execute("BEGIN")
            self._intrans = True
        finally:
            curs.close()

        if loginfo is not None:
            self._logger.log_stmt("TRANSACTION BEGIN {0}".format(loginfo))

    def commit_transaction(self, loginfo : str = None):
        if not self._intrans:
            raise Exception("No transaction started in commit_transaction()")
        curs = self.conn.cursor()
        try:
            curs.execute("COMMIT")
            self._intrans = False
        finally:
            curs.close()

        for dco in self._transafterdels:
            self._doafterdel(dco)
            
        self._transafterdels.clear()

        if loginfo is not None:
            self._logger.log_stmt("TRANSACTION COMMIT {0}".format(loginfo))

    def rollback_transaction(self, loginfo : str = None):
        if not self._intrans:
            raise Exception("No transaction started in rollback_transaction()")
        
        curs = self.conn.cursor()
        try:    
            curs.execute("ROLLBACK")
            self._intrans = False
        finally:
            curs.close()
            
        if loginfo is not None:
            self._logger.log_stmt("TRANSACTION ROLLBACK {0}".format(loginfo))

    def _gettablename(self, pinst : PBase):
        return pinst.__class__._getclstablename()

    def try_createtable(self, pclass) -> bool:
        try:
            self.createtable(pclass)
            answ = True
        except Exception as exc:
            self._logger.log_stmt(str(exc))
            answ = False
        
        return answ

    def set_db_dbglevel(self, filepath : str, levelstr : str):
        if type(levelstr) is str:
            lowlev = levelstr.lower()
            if lowlev == "none":
                level = DbgStmtLevel.NONE
            elif lowlev == "stmts":
                level = DbgStmtLevel.STMTS
            elif lowlev == "datafill":
                level = DbgStmtLevel.DATAFILL
            else:
                raise Exception("unknown debuglevel <{0}>".format(levelstr))
            self._logger = SQPLogger(filepath, level)
        else:
            raise Exception("unexpected parametertype for database debug level. Use str here")

    def try_droptable(self, pinstclass):
        try:
            self.droptable(pinstclass)
        except:
            pass

    def _get_uniquegrps(self, cls : Type) -> dict:
        answ = {}
        cd = cls._classdict[cls]
        for key, val in cd.items():
            decl = val.get_declaration()
            grpname = decl.__getattribute__("_uniquegrp")
            if grpname is None:
                continue

            if grpname not in answ:
                answ[grpname] = [key] #start a list containing keys which are in the group
            else:
                answ[grpname].append(key) #append key to the already existing key-tuple

        return answ

    def createtable(self, pinstcls):
        pinst = pinstcls()
        tablename = pinstcls._getclstablename()
        memd = pinstcls._classdict[pinstcls]
        unigrps = self._get_uniquegrps(pinstcls)
        collst = "("
        first = True
        for key, val in memd.items():
            decl = val.get_declaration()
            #do not create columns for unwritable declarations like EmbeddedJoinedList....
            if not decl.is_dbstorable(): 
                continue

            if first:
                collst += key + " " + self._get_dbtypename(val)
                first = False
            else:
                collst += "," + key + " " + self._get_dbtypename(val)

            if key == "_id": #id is always the primary key and nothing else
                collst += " PRIMARY KEY"

        for name, columns in unigrps.items():
            collst += ", CONSTRAINT {0} UNIQUE(".format(name)
            first = True
            for col in columns:
                if first:
                    collst += col
                    first = False
                else:
                    collst += ", " + col

            collst += ")"

        collst += ")"

        cursor = self.conn.cursor()
        try:
            exs = "CREATE TABLE {0} {1}".format(tablename, collst)
            self._logger.log_stmt("EXEC: {0}", exs)
            cursor.execute(exs)
        except Exception as exc:
            self._logger.log_stmt("ERROR: {0}", str(exc))
            raise exc
        finally:
            cursor.close()

    def droptable(self, pinstcls):
        """drop a table which had been created for the given class"""
        tablename = pinstcls._getclstablename()
        try:
            cursor = self.conn.cursor()
            exs = "DROP TABLE {0} ".format(tablename)
            self._logger.log_stmt("EXEC: {0}", exs)
            cursor.execute(exs)
        except Exception as exc:
            self._logger.log_stmt("ERROR: {0}", str(exc))
        finally:
            cursor.close()

    def _doafterdel(self, dco):
        cls = dco.__class__
        if hasattr(cls, "on_after_delete") and callable(getattr(cls, "on_after_delete")):
            dco.on_after_delete()
            
    def delete(self, dco):
        """Delete the given persitent instance and do all the casscading deletes (if any). 
        Make sure that neither all the deletes du execute or none by using transactions behind the
        scenes"""
        curs = self.conn.cursor()
        microtrans = not self._intrans
        if microtrans:
            self.begin_transaction("delete cascade")
        try:
            try:
                self._notransdeletecascaded(curs, dco)
                if microtrans:
                    self.commit_transaction("delete cascade")
            except Exception as err:
                if microtrans:
                    self.rollback_transaction(str(err))
                raise Exception(str(err))
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
                self.fill_joins(dco, decl)
                loco = getattr(dco, membkey)
                if not loco is None:
                    self._notransdeletecascaded(curs, loco)

            elif issubclass(declt, JoinedEmbeddedList) and decl.get_cascadedelete():
                self.fill_joins(dco, decl)
                locos = getattr(dco, membkey)
                for loco in locos:
                    self._notransdeletecascaded(curs, loco)

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
        stmt = "DELETE FROM {0} WHERE _id=?".format(tablename)
        self._logger.log_stmt("EXEC: {0}", stmt)
        curs.execute(stmt, (dco._id,))
        self._transafterdels.append(dco)

    def _get_dbtypename(self, val):
        ot = val.get_outertype()
        if ot == None:
            return "NONE"
        else:
            return ot.name

       
    def getcat(self, cls : PCatalog, code : str, lang:str=None):
        """Get a full catalog entry of the given type and code. If the cat is language sensitive the code
            will be searched in the current language of the factory

            lang can be override to enforce a language other then the current language of the factory for
            language sensitive catalogs
        """
        if lang is None:
            if cls.is_langsensitive():
                mylang = self.lang
            else:
                mylang = "*?NOLANG?*"
        else:
            mylang = lang

        cattype = cls._cattype

        ck = self._createcachekey(mylang, cattype, code)

        if ck in self._catcache:
            return self._catcache[ck]

        ce = self._readcatentryfromdb(cls, cattype, mylang, code)
        self._catcache[ck] = ce
        return ce

    def _detect_lst_change(self, newl, oldl):
        newnoid = list(filter(lambda el : el._id is None, newl))
        newhasid = list(filter(lambda el : el._id is not None, newl))
        newids = list(map(lambda el : el._id, newhasid))
        oldids = list(map(lambda el : el._id, oldl))
        newonly = []
        oldonly = []
        both = []
        both_ids = []

        for newele in newhasid:
            if newele._id in oldids:
                oldele = list(filter(lambda el : el._id==newele._id, oldl))[0]
                both.append((newele, oldele))
                both_ids.append(newele._id)
            else:
                newonly.append(newele)

        for oldele in oldl:
            if oldele._id not in newids and oldele._id not in both_ids:
                oldonly.append(oldele)

        newonly.extend(newnoid) 
        
        return newonly, oldonly, both


    def flush_diffs(self, newp, oldp):
        """ flush everything so that newp is completely persistet. Any list elements not present
            in oldp will be deleted during flush_diffs
            This is done deep! 
        """
        newt = type(newp)
        oldt = type(oldp)
        if newt != oldt:
            raise Exception("flush_diffs: types are not the same {} vs. {}".format(str(newt), str(oldt))) #not same types, no diff no flush!
        if newp._id is None:
            raise Exception("flush_diffs: new id is None for element type {}".format(str(newt))) #no id no flushdiff!
        if oldp._id is None:
            raise Exception("flush_diffs: old id is None for element type {}".format(str(oldt))) #no id no flushdiff!
        if newp._id != oldp._id:
            raise Exception("flush_diffs: ids are different") #not same id, no flushdiff!

        self.flush(newp)
        mdict = newp._get_my_memberdict()

        for mdname, mdentry in mdict.items():
            if mdentry._dectype is JoinedEmbeddedObject:
                newembedo = getattr(newp, mdname)
                oldembedo = getattr(oldp, mdname)
                if newembedo is not None and oldembedo is not None:
                    self.flush_diffs(newembedo, oldembedo)
                elif newembedo is not None:
                    self.flush(newembedo)
                
            elif mdentry._dectype is JoinedEmbeddedList or mdentry._dectype is IntersectedList:
                newlstatt = getattr(newp, mdname)
                oldlstatt = getattr(oldp, mdname)
                newonlylst, oldonlylst, bothlst = self._detect_lst_change(newlstatt, oldlstatt)
                # bothlst contains tuples of (old,new)
                for elm in bothlst: #bothlist is a list of tuples (old, new)
                    self.flush_diffs(elm[0], elm[1]) #at 0 is new, at 1 is old
                for elm in newonlylst:
                    self.flush(elm)
                for elm in oldonlylst:
                    if elm._id is not None: #if exists in DB
                        self.delete(elm)

                

    def flushcopy(self, pinst):
        """ Flush the instance but make sure we have a new insert even 
            if we have been flushing before. This a new _id
            will be created
        """
        pinst._id = None
        self.flush(pinst)

    def flush(self, pinst : PBase):
        """write the instance to the database inserting or updating as needed"""

        if not pinst.has_changed():
            return

        curs = self.conn.cursor()
        microtrans = not self._intrans
        try:
            curs = self.conn.cursor()
            if microtrans:
                self.begin_transaction("flush")
            try:
                if pinst._id is None: #we need to insert
                    pinst._id = uuid.uuid4()
                    pinst.created = dt.datetime.now()
                    pinst.lastupdate = dt.datetime.now()
                    self._insert(curs, pinst)
                    if curs.rowcount!=1:
                        raise Exception("Insert of a single persistent object failed, {} rows were changed on last update".format(curs.rowcount))
                else: #we need to update
                    pinst.lastupdate = dt.datetime.now()
                    self._update(curs, pinst)
                    if curs.rowcount!=1:
                        raise Exception("Update of a single persistent object failed, {} rows were changed on last update".format(curs.rowcount))

                if microtrans:
                    self.commit_transaction("flush")
            except sq3.Error as err:
                if microtrans:
                    self.rollback_transaction(str(err))
                raise Error(str(err))
        finally:
            curs.close()


    def _getinsertvaluestuple(self, pinst):
        pinstcls = pinst.__class__
        memd = pinstcls._classdict[pinstcls]
        first = True
        valtuplst = []
        for key, val in memd.items():
            propvalue = pinst.__getattribute__(key)
            
            if propvalue is not None:
                dt = val.get_declaration()
                if dt.is_dbstorable():
                    if issubclass(type(propvalue), PCatalog):
                        propvalue = propvalue.code

                    valtuplst.append(propvalue)
                    if first:
                        first = False
                        cquests = "?"
                        cnames = key
                    else:
                        cquests += ", ?"
                        cnames += ", " + key

        return tuple(valtuplst), cnames, cquests

    def _getupdatevaluestuple(self, pinst):
        """get a everything for the update statement omitting _id, created bur having lastupdate on the
         current date and time
         _id is last in valuestuple but not mentioned in csets!"""
        pinstcls = pinst.__class__
        memd = pinstcls._classdict[pinstcls]
        first = True
        valtuplst = []
        for key, val in memd.items():
            data = val.get_declaration()
            if data.is_dbstorable():
                if key not in ("_id", "created"):
                    if key != "lastupdate":
                        propvalue = pinst.__getattribute__(key)
                    else:
                        propvalue = dt.datetime.now()

                    if issubclass(type(propvalue), PCatalog):
                        propvalue = propvalue.code
                        
                    valtuplst.append(propvalue)
                    if first:
                        first = False
                        csets = key + "=?"
                    else:
                        csets += ", " + key + "=?"

        valtuplst.append(pinst._id)
        return tuple(valtuplst), csets

    def _insert(self, curs, pinst : PBase):
        table = self._gettablename(pinst)
        valtuple, inscolnames, inscolquests = self._getinsertvaluestuple(pinst)
        curs.execute("INSERT INTO " + table + "(" + inscolnames + ") values (" + inscolquests + ")", valtuple)

    def _update(self, curs, pinst : PBase):
        tablename = self._gettablename(pinst)
        valtuple, csets = self._getupdatevaluestuple(pinst)
        stmt = "UPDATE {0} SET {1} WHERE _id=?".format(tablename, csets)
        curs.execute(stmt, valtuple)

    def find(self, cls, findpar = None, orderlist=None, limit=0):
        """Find the data
        
        """
        if findpar is None: #do a select * eventually respecting limit but with no where clause
            return self._do_select(cls, findpar, orderlist, limit)
        elif type(findpar) is dict:
            return self._do_select(cls, findpar,  orderlist, limit)
        elif issubclass(type(findpar), PBase): #we have an object which shuld be read agoin from the db
            if findpar._id is None:
                raise Exception("SqFactory.find() with an Mpbase derived instance only works when this instance contains an _id")

            res = self.find_with_dict(cls, {"_id": findpar._id})
            return self._first_or_default(res)
        elif findpar is uuid.UUID: #we have an id to be searched for
            res = self.find_with_dict(cls, {"_id": findpar})
            return self._first_or_default(res)
        else:
            raise NotImplementedError("Unsupported type <{}> in findpar.".format(type(findpar)))

    def _get_order_dir(self, od : OrderDirection) -> str:
        if od is OrderDirection.ASCENDING:
            return ""
        elif od is OrderDirection.DESCENDING:
            return " DESC"
        else:
            raise Exception("unknpwn order direction!")

    def _do_select(self, cls, findpar, orderlist, limit):
        stmt = "SELECT * FROM {0}".format(cls._getclstablename())

        if findpar is not None:
            if len(findpar) > 0:
                wc = self._create_where(findpar)
                if not wc is None:
                    stmt += " WHERE " + wc                    

        if limit is not None and limit >0:
            if findpar is None:
                stmt += " WHERE ROWNUM < " + str(limit)
            else:
                stmt += " AND ROWNUM<" + str(limit)

        if orderlist is not None:
            stmt += " ORDER BY "
            first = True
            for order in orderlist:
                if first:
                    first = False
                    stmt += order[0] + self._get_order_dir(order[1])
                else:
                    stmt += ", " + order[0] + self._get_order_dir(order[1])

        self._logger.log_stmt("EXEC: {0}", stmt)
        curs = self.conn.cursor()
        try:
            answ = curs.execute(stmt)
        except OperationalError as oe:
            self._logger.log_stmt("ERROR: {0}", str(oe))
            raise Exception(stmt + " " + str(oe))
        #finally:
        #    curs.close()

        return answ

    def _backmap(self, ops):
        mapping = {"$eq":"=", 
            "$neq":"<>",
            "$gt":">",
            "$lt":"<",
            "$gte":">=",
            "$lte":"<=",
            "$nin": "NOT IN",
            "$in": "IN",
            "$and" : "AND",
            "$or": "OR"}
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
            return "'{0}'".format(operand.hex)
        elif t is dict:
            return self._getoperanddict(operand)
        elif t is dt.datetime:
            return "datetime('{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}.{6}')".format(operand.year, operand.month, operand.day, operand.hour, operand.minute, operand.second, operand.microsecond)
        elif t is bool:
            return operand
        elif t is list:
            answ = "("
            first = True
            for lel in operand:
                if first:
                    answ += self._getoperand(lel)
                    first = False
                else:
                    answ += ", " + self._getoperand(lel)
            answ += ")"
            return answ
        else:
            raise Exception("unknown operand type {0} in _getoperand()".format(str(t)))

    def _getoperanddict(self, operand):
        operandl = list(operand.items())
        op = operandl[0][0]
        right = operandl[0][1]
        tr = type(right)
        if self._ismulti(op):
            return self._getmultipart(op, right)
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
                #answ += " AND "
                answ += " " + self._backmap(op) + " "
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

        #handle the all-is-on-level-0 type here
        if type(oplist) is dict:
            return self._getoperanddict(findpar)

        if not type(oplist) is list:
            raise Exception("first layer value must be a dictionary containing the operands")

        if self._ismulti(op):
            answ = self._getmultipart(op, oplist)            
        elif self._isbinary(op):
            answ = self._getbinarypart(op, oplist)

        return answ


    def _readcatentryfromdb(self, catcls, cattype : str, lang : str, catcode : str):
        """read a single catlog entry from the database"""
        if lang != "*?NOLANG?*":
            stmt = "SELECT * FROM {0} where type=? and code=? and langcode=?".format(catcls._getclstablename())
            parat = (cattype, catcode, lang)
        else:
            stmt = "SELECT * FROM {0} where type=? and code=?".format(catcls._getclstablename())
            parat = (cattype, catcode)
        
        curs = self.conn.cursor()
        try:
            self._logger.log_stmt("EXEC: {0}", stmt)
            rows = curs.execute(stmt, parat)
            ct = 0
            for row in rows:
                answ = self._create_instance(catcls, row)
                ct += 1
                if ct > 1:
                    self._logger.log_stmt("ERROR: Catalog Code <{0}> not unique", catcode)
                    raise Exception("Catalog code <{0}> is not unique in catalog-type <{1}> for class {2} in language <{3}>".format(catcode, 
                            cattype,
                            str(catcls), 
                            lang))

            if ct == 0:
                self._logger.log_stmt("ERROR: Catalog Code <{0}> not found", catcode)
                raise Exception("Catalog code <{0}> not found in catalog-type <{1}> for class {2} in language <{3}>".format(catcode, 
                            cattype,
                            str(catcls), 
                            lang))

        finally:
            curs.close()

        return answ

    def _createcachekey(self, lang, cattype, catcode):
        return lang + "#" + cattype + "#" + catcode

    def _get_fullcatentry(self, decl : ClassDictEntry, dbdta) -> PCatalog:
        """interpret dbdata as a key to catlog entry of a type declared/given in decl
            and return the full catalog-entry. Do minimize db-access the catalogentries are cached
            internally.

        """
        if dbdta is None:
            return None

        catdef = decl.get_declaration()
        catcls = decl.get_dectype()
        catcode = str(dbdta)
        catpersisttype = catdef._catalogtype
        if catpersisttype.is_langsensitive():
            lang = self.lang
        else:
            lang = "*?NOLANG?*"

        cattype = catpersisttype._cattype
        cachekey = self._createcachekey(lang, cattype, catcode)
        if cachekey in self._catcache:
            answ = self._catcache[cachekey]
        else:
            answ = self._readcatentryfromdb(catpersisttype, cattype, lang, catcode)
            self._catcache[cachekey] = answ

        return answ

    def _create_instance(self, cls : PBase, row):
        """create an instance of the object with a cursor to a selected row as row
        """
        inst = cls()
        inst._dbvaluescache = {} #create a new cahce fpr the old values as read from db
        vd = inst._get_my_memberdict()

        jembs = []
        jlists = []
        ilists = []
        for key, value in vd.items():
            #if hasattr(inst, key) and getattr(inst, key) is not None:
            #    continue
            
            decl = value._declaration
            declt = type(decl)
            
            if declt is JoinedEmbeddedObject:
                if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                    jembs.append(decl)
            elif declt is JoinedEmbeddedList:
                if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                    jlists.append(decl)
            elif declt is IntersectedList:
                if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                    ilists.append(decl)
            elif declt is Catalog:
                dbdta = row[key]
                cate = self._get_fullcatentry(value, dbdta)
                setattr(inst, key, cate)
                inst._dbvaluescache[key] = cate
            elif declt is Blob:
                dbdta = row[key]
                self._logger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, "blobdata..."))
                try:
                    blobby = decl.to_innertype(dbdta)
                    setattr(inst, key, blobby)
                    inst._dbvaluescache[key] = blobby
                except Exception as ex:
                    self._logger.log_dtafill("ERROR: <{0}> contents: <{1}> - Originalmeldung {2}".format(key, dbdta, str(ex)))
                    raise Exception("Unerwarteter Fehler beim Versuch das Feld {0} einer Instanz der Klasse {1} mit <{2}> zu füllen. Originalmeldung: {3}".format(key, decl, "blobdata...", str(ex)))
            else:
                dbdta = row[key]
                self._logger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, dbdta))
                try:
                    inty = decl.to_innertype(dbdta)
                    setattr(inst, key, inty)
                    inst._dbvaluescache[key] = inty
                except Exception as ex:
                    self._logger.log_dtafill("ERROR: <{0}> contents: <{1}> - Originalmeldung {2}".format(key, dbdta, str(ex)))
                    raise Exception("Unerwarteter Fehler beim Versuch das Feld {0} einer Instanz der Klasse {1} mit <{2}> zu füllen. Originalmeldung: {3}".format(key, decl, dbdta, str(ex)))

        for jemb in jembs:
            self._fill_embedded_object(inst, jemb)

        for jlist in jlists:
            self._fill_embedded_list(inst, jlist)

        for ilist in ilists:
            self._fill_intersected_list(inst, ilist)

        return inst

    def get_contents(self, pinst, chk):
        """ get the contents of a field when chk is a field definition or the
            contents of the member when chk is a member name"""
        if type(chk) is str:
            return pinst.__getattribute__(chk)
        elif issubclass(type(chk), BaseVarType):
            localidfieldname = chk.get_fieldname()
            return pinst.__getattribute__(localidfieldname)
        else:
            raise Exception("Definition error for class {}. Field must be named by its name as a string or by its definition".format(str(type(pinst))))

    def _fill_embedded_object(self, pinst : PBase, jdef : JoinedEmbeddedObject):
        tgtfieldname = jdef.get_fieldname()
        if tgtfieldname is None:
            raise Exception("targetfield name cannot be derived during fill of a joined embedded object")

        if pinst.__getattribute__(tgtfieldname) is not None:
            return

        tgtcls = jdef.get_targettype()
        if tgtcls is None:
            raise Exception("missing targettype in JonedEmbeddedObject during fill")

        localid = self.get_contents(pinst, jdef._localid)
        # localidfielddef = jdef._localid
        # localidfieldname = localidfielddef.get_fieldname()
        # localid = pinst.__getattribute__(localidfieldname)
        if localid is None:
            return

        #we cannot use QQuery here because that would produce circular imports
        tablename = tgtcls._getclstablename()
        stmt = "SELECT * from {0} where {1}=?".format(tablename, jdef._foreignid)
        self._logger.log_stmt("EXEC: {0}", stmt)
        curs = self.conn.cursor()
        try:
            rows = curs.execute(stmt, (localid,)) #self._getoperand(localid)
            ct = 0
            for row in rows:
                ct += 1
                firstrow = row

            if ct == 0:
                raise Exception("join of field {0} found no target".format(tgtfieldname))

            if ct > 1:
                raise Exception("join on field {0} found multiple targets".format(tgtfieldname))

            tgtinst = self._create_instance(tgtcls, firstrow)
            pinst.__setattr__(tgtfieldname, tgtinst)
        finally:
            curs.close()

    def _fill_intersected_list(self, pinst : PBase, idef : IntersectedList):
        tgtfieldname = idef.get_fieldname()
        if tgtfieldname is None:
            raise Exception("targetfield name cannot be derived during fill of a joined embedded list")

        if pinst.__getattribute__(tgtfieldname) is not None:
            return

        tgtcls = idef.get_targettype()

        localid = self.get_contents(pinst, idef._localid)
        if localid is None:
            pinst.__setattr__(tgtfieldname, [])
            return

        intertablename = tgtcls._getclstablename()
        upfieldname = idef.get_up_keyname()

        stmt = "SELECT * from {} where {}=?".format(intertablename,
            upfieldname)

        addw = tgtcls.additional_where()
        if addw is not None:
            qdg = SQQueryDictGenerator()
            qdict = qdg.getquerydict(addw)
            stmt += " AND " +  self._create_where(qdict)

        self._logger.log_stmt("EXEC: {0}", stmt)
        curs = self.conn.cursor()
        try:
            rows = curs.execute(stmt, (localid,)) #self._getoperand(localid)
            ct = 0
            scratchl = []
            for row in rows:
                tgtinst = self._create_instance(tgtcls, row)
                scratchl.append(tgtinst)

            pinst.__setattr__(tgtfieldname, scratchl)
            
        finally:
            curs.close()


    def _fill_embedded_list(self, pinst : PBase, jdef : JoinedEmbeddedList):
        tgtfieldname = jdef.get_fieldname()
        if tgtfieldname is None:
            raise Exception("targetfield name cannot be derived during fill of a joined embedded list")

        if pinst.__getattribute__(tgtfieldname) is not None:
            return

        tgtcls = jdef.get_targettype()
        if tgtcls is None:
            raise Exception("missing targettype in JoinedEmbeddedList during fill")

        if not type(jdef._localid):
            localidfielddef = jdef._localid
            localidfieldname = localidfielddef.get_fieldname()
        else:
            localidfieldname = jdef._localid

        localid = pinst.__getattribute__(localidfieldname)
        if localid is None:
            pinst.__setattr__(tgtfieldname, [])
            return

        #we cannot use QQuery here because that would produce circular imports
        tablename = tgtcls._getclstablename()
        tgtforeignfieldname = jdef.get_foreign_keyname()
        stmt = "SELECT * from {0} where {1}=?".format(tablename, tgtforeignfieldname)
        self._logger.log_stmt("EXEC: {0}", stmt)
        curs = self.conn.cursor()
        try:
            rows = curs.execute(stmt, (localid,)) #self._getoperand(localid)
            ct = 0
            scratchl = []
            for row in rows:
                tgtinst = self._create_instance(tgtcls, row)
                scratchl.append(tgtinst)

            pinst.__setattr__(tgtfieldname, scratchl)
            
        finally:
            curs.close()

    def fill_joins(self, pinst : PBase, *args):
        """fill the joins on the instance class given by args
        use like fact.filljoins(myinst, MyInstClass.Join01, MyInstClass.Join02, ...)"""

        for arg in args:
            targ = type(arg)
            if targ is JoinedEmbeddedList:
                self._fill_embedded_list(pinst, arg)
            elif targ is JoinedEmbeddedObject:
                self._fill_embedded_object(pinst, arg)
            elif targ is IntersectedList:
                self._fill_intersected_list(pinst, arg)
            else:
                raise Exception("argument {0} is no joined definition".format(str(arg)))

    @classmethod
    def adapt_uuid(cls, gid):
        return gid.hex

    @classmethod
    def convert_uuid(cls, text):
        if text.decode() == 'None':
            return None
        else:
            return uuid.UUID(hex=text.decode())






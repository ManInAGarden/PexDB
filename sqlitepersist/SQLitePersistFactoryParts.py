import sqlite3 as sq3
import uuid
import datetime

from sqlitepersist.SQLitePersistBasicClasses import DbType, PBase


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

    @classmethod
    def adapt_uuid(cls, gid):
        return gid.hex

    @classmethod
    def convert_uuid(cls, text):
        if text.decode() == 'None':
            return None
        else:
            return uuid.UUID(hex=text.decode())




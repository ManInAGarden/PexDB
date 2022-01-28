from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *



class NoneFoundException(Exception):
    pass

class OrderInfo(object):
    def __init__(self, field, direction : OrderDirection):
        self.field = field
        self.orderdir = direction

class SQQueryIterator():
    def __init__(self, sqpq):
        self._sqpq = sqpq
        self._sqlcursor = None

    def __next__(self):
        if self._sqlcursor is None:
            self._sqlcursor = self._sqpq.finddata()
        
        cn = self._sqlcursor.__next__()

        dco = self._sqpq._sqf._create_instance(self._sqpq._cls , cn)

        if self._sqpq._selfunc is not None:
            dco = self._sqpq._selfunc(dco)

        return dco

class SQQuery():
    

    def __init__(self, fact : SQFactory, cls : BaseVarType):
        self._sqf = fact
        self._cls = cls
        self._whereop = None
        self._order = None
        self._selfunc = None

    def where(self, express = None):
        """Creates data to store the where part.
           This gets used when the db select statement is produced and executed later on"""
        addw = self._cls.additional_where()
        if issubclass(type(express), SpecialWhereInfo):
            wo = OperationStackElement(express.get_left(), express.get_op(), express.get_right())
        else:
            wo = express

        if wo is not None:
            if addw is not None:
                self._whereop = OperationStackElement(wo, "&", addw)
            else:
                self._whereop = wo
        else:
            if addw is not None:
                self._whereop = addw
            else:
                self._whereop = None

        return self

    def first_or_default(self, default):
        """get first element of the query result

           When no result can be foudn the default is returned
           instead.

           parameters
           ----------

           default: a default which will be returned instead of raising an exception in case no
           results can be found

           Returns
           -------

           The first element of the query result
        """
        try:
            return self.first()
        except NoneFoundException as nexc:
            return default

    def first(self):
        """get first element of the query result

           When no result can be found an exception is raised

           Returns
           -------

           The first element of the query result
        """
        firstel = None
        for el in self:
            firstel = el
            if firstel is not None:
                break

        if firstel is None:
            raise NoneFoundException("No data found in database with first(), consider use of first_or_defauöt()")

        return firstel

    def as_list(self):
        return list(self)

    def order_by(self, *args):
        """creates the order part in form a list of OrderInfos to be used when the db select-statement gets
        produced and executed"""
        self._order = []

        for arg in args:
            tolm = type(arg)

            if issubclass(tolm, BaseVarType):
                oi = OrderInfo(arg, OrderDirection.ASCENDING)
            elif tolm is OrderInfo:
                oi = arg

            self._order.append(oi)

        return self

    def select(self, selfunc):
        """The select method of the query
            transforms the originally selected data instances to
            whatever the selfunc does
            Here the method is stored for later use in the iterator when the
            instances are actually instantiated.
        """
        self._selfunc = selfunc
        return self

    def __iter__(self):
        ''' Returns the Iterator object '''
        return SQQueryIterator(self)

    def finddata(self):
        """this generates and executes the statement
            (in reality it asks the factory to execute statement)
            and returns a cursor to the selected data
        """
        qdict, orderlist = self._generateall()
        return self._sqf.find(self._cls, qdict, orderlist)

    def _generateall(self):
        qdg = SQQueryDictGenerator()

        qdict = qdg.getquerydict(self._whereop)
        orderl = self._generateorderlist(self._order)
        return qdict, orderl

    def _generateorderlist(self, ol):
        if ol is None: return None
        if len(ol) <= 0: return None

        answ = []
        for olm in ol:
            answ.append(self._getorder(olm))

        return answ

    def _getorder(self, olm : OrderInfo):
        field = olm.field
        fieldname = getvarname(field)
        return (fieldname, olm.orderdir)


    

    
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *



class NoneFoundException(Exception):
    pass

class OrderInfo(object):
    def __init__(self, field, direction : str):
        self.field = field
        self.orderdir = direction

class SpecialWhereInfo(object):
    def __init__(self, field, infotype, infodata):
        self._field = field
        self._infotype = infotype
        self._infodata = infodata

    def __and__(self, other):
        return OperationStackElement(self, "&", other)

    def __or__(self, other):
        return OperationStackElement(self, "|", other)

    def __invert__(self):
        return OperationStackElement(None, "~", self)

    def get_left(self):
        return self._field

    def get_right(self):
        return self._infodata

    def get_op(self):
        return self._infotype

class IsIn(SpecialWhereInfo):
    def __init__(self, field, infodata):
        super().__init__(field, infotype="ISIN", infodata=infodata)

class NotIsIn(SpecialWhereInfo):
    def __init__(self, field, infodata):
        super().__init__(field, infotype="NOTISIN", infodata=infodata)

class Regex(SpecialWhereInfo):
    def __init__(self, field, infodata):
        super().__init__(field, infotype="REGEX", infodata=infodata)


class SQQueryIterator():
    def __init__(self, sqpq):
        self._sqpq = sqpq
        self._sqlcursor = None
        #self._index = 0

    def __next__(self):
        if self._sqlcursor is None:
            self._sqlcursor = self._sqpq.finddata()
        
        cn = self._sqlcursor.__next__()

        dco = self._sqpq._sqf._create_instance(self._sqpq._cls , cn)
        #if self._index >= len(self._datalist):
        #    raise StopIteration

        #nextv = self._datalist[self._index]

        if self._sqpq._selfunc is not None:
            dco = self._sqpq._selfunc(dco)

        #self._index += 1
        return dco


    

class SQQuery():
    opmapping = {"==":"$eq", 
            "!=":"$neq",
            ">":"$gt",
            "<":"$lt",
            ">=":"$gte",
            "<=":"$lte"}
    logmapping = {"&":"$and",
            "|":"$or",
            "~" : "$not"}
    specsmapping = {"ISIN":"$in",
        "NOTISIN":"$nin",
        "REGEX": "$regex"}

    def __init__(self, fact : SQFactory, cls : BaseVarType):
        self._sqf = fact
        self._cls = cls
        self._whereop = None
        self._order = None
        self._selfunc = None

    def where(self, express = None):
        """Creates data to store the where part.
           This gets used when the db select statement is produced and executed later on"""
        if issubclass(type(express), SpecialWhereInfo):
            self._whereop = OperationStackElement(express.get_left(), express.get_op(), express.get_right())
        else:
            self._whereop = express
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

    def order_by(self, *args):
        """creates the order part in form a list of OrderInfos to be used when the db select-statement gets
        produced and executed"""
        self._order = []

        for arg in args:
            tolm = type(arg)

            if issubclass(tolm, BaseVarType):
                oi = OrderInfo(arg, "asc")
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
        qdict = self._getquerydict(self._whereop)
        orderl = self._generateorderlist(self._order)
        return qdict, orderl

    def _generateorderlist(self, ol):
        if ol is None: return None
        if len(ol) <= 0: return None

        answ = []
        for olm in ol:
            answ.append(self._getorder(olm))

        return answ

    def _getorder(self, olm):
        field = olm.field
        if olm.orderdir == "asc":
            dir = OrderDirection.ASCENDING
        elif olm.orderdir == "desc":
            dir = OrderDirection.DESCENDING
        else:
            raise Exception("Unknown ordering direction <{}> in _getorder()".format(olm._order))

        fieldname = getvarname(field)
        return (fieldname, dir)

        

    def _getquerydict(self, op):
        if op is None:
            return {} #no query supplied -> query all

        leftpart = self._getpart(op._left)
        rightpart = self._getpart(op._right)
        oppart = self._getop(op._op)

        if oppart in self.logmapping.values():
            if oppart != "$not":
                return {oppart:[leftpart, rightpart]}
            else:
                return self._notted(rightpart)
        elif oppart in self.opmapping.values():
            return {leftpart:{oppart: rightpart}}
        elif oppart in self.specsmapping.values():
            return {leftpart:{oppart: rightpart}}
        else:
            raise Exception("Uuuuuups in _getquerydict")
        
    def _notted(self, rdict):
        if not type(rdict) is dict:
            raise Exception("Expected dictionary in _notted() but received {}".format(type(rdict).__name__))

        if len(rdict)!=1:
            raise Exception("Expected dictionary of len 1 in _notted() but received len {}".format(len(rdict)))
        
        for key, val in rdict.items():
            return {key : {"$not" : val}}

    def _getop(self, op):
        mapping = {**self.opmapping, **self.logmapping, **self.specsmapping} #merge mappings
        
        if not op in mapping.keys():
            raise Exception("Unknown operator <{}>".format(op))

        return mapping[op]

    def _getpart(self, part):
        t = type(part)
        if t is OperationStackElement:
            part = self._getquerydict(part)
        elif issubclass(t, BaseVarType):
            part = getsubedvarname(part)
        elif t is Val:
            part = part._value
        elif issubclass(t, SpecialWhereInfo):
            part = self._getspecialdict(part)

        return part

    def _getspecialdict(self, part):
        if part is None:
            return {} #no query supplied -> query all

        leftpart = part.get_left()
        rightpart = part.get_right()
        oppart = part.get_op()
        oppart = self._get_special_op(oppart)

        if issubclass(type(leftpart), BaseVarType):
            leftpart = getsubedvarname(leftpart)

        if issubclass(type(rightpart), BaseVarType):
            rightpart = getsubedvarname(rightpart)

        if oppart in self.specsmapping.values():
            return {leftpart:{oppart: rightpart}}
        else:
            raise Exception("Uuuuuups in _getspecialdict")

    def _get_special_op(self, oppart):
        if not oppart in self.specsmapping.keys():
            raise Exception("Special opration <{}> not supported in _get_special_op()".format(oppart))

        return self.specsmapping[oppart]
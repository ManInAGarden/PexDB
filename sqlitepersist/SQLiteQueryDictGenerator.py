from .SQLitePersistBasicClasses import *

class SQQueryDictGenerator:
    """ class to create a query dict from an OperationStack
    """
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

    def __init__(self):
        self.mapping = {**self.opmapping, **self.logmapping, **self.specsmapping} #merge mappings

    def getquerydict(self, op):
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

    def _getpart(self, part):
        t = type(part)
        if t is OperationStackElement:
            part = self.getquerydict(part)
        elif issubclass(t, BaseVarType):
            oldpart = part
            part = getsubedvarname(part)
            if part is None:
                raise Exception("Varname not found for part of type {} with varcode {}".format(str(type(oldpart)), str(oldpart._varcode)))
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

    def _getop(self, op):
        if not op in self.mapping.keys():
            raise Exception("Unknown operator <{}>".format(op))

        return self.mapping[op]
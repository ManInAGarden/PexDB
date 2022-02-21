import datetime as dt
from email.policy import default
import uuid
import inspect
from enum import Enum, unique

from urllib3 import Retry

class DbType(Enum):
     NULL = 0 
     INTEGER = 1
     REAL = 2
     TEXT = 3
     BLOB = 4
     TIMESTAMP = 5

class OrderDirection(Enum):
    ASCENDING=0
    DESCENDING=1

class OperationStackElement(object):
    def __init__(self, left, op, right):
        self._left = left
        self._right = right
        self._op = op

    def __and__(self, other):
        return OperationStackElement(self, "&", other)

    def __or__(self, other):
        return OperationStackElement(self, "|", other)

    def __eq__(self, other):
        return OperationStackElement(self, "==", other)

    def __neq__(self, other):
        return OperationStackElement(self, "!=", other)

    def __str__(self):
        return "op " + str(self._left) + self._op + str(self._right)
     
class BaseComparableType(object):
    def __init__(self):
        pass

    def __eq__(self, other):
        return OperationStackElement(self, "==", other)

    def __neq__(self, other):
        return OperationStackElement(self, "!=", other)

    def __lt__(self, other):
        return OperationStackElement(self, "<", other)

    def __le__(self, other):
        return OperationStackElement(self, "<=", other)

    def __gt__(self, other):
        return OperationStackElement(self, ">", other)

    def __ge__(self, other):
        return OperationStackElement(self, ">=", other)

class Val(BaseComparableType):
    def __init__(self, value):
        self._value = value

class BaseVarType(BaseComparableType):
    _innertype = None #type in instance
    _outertype = None #type in database
    _subclasses = []
    _myfieldname = None #used to cache a field name once it was searched by get_fieldname()

    def __init__(self, **kwarg):
        super().__init__()
        self._subdef = None
        self._varcode = uuid.uuid4()
        self._getpara(kwarg, "default")
        self._getpara(kwarg, "defaultgenerator")
        self._getpara(kwarg, "uniquegrp")
        
    def get_default(self):
        if self._defaultgenerator is None:
            return self._default
        else:
            return self._defaultgenerator()

    def to_innertype(self, dta):
        raise Exception("Override me in <BaseType.to_innertype() in declration-type {}".format(type(self).__name__))

    def get_fieldname(self):
        if self._myfieldname is not None: return self._myfieldname

        vname = getvarname(self)
        self._myfieldname = vname
        return vname

    def is_dbstorable(self):
        return True

    def _getpara(self, kwargs, name, default=None, excstr=None):
        membername = "_" + name
        done = False
        if name in kwargs.keys():
            setattr(self, membername, kwargs[name])
            done = True
        elif default is not None:
            setattr(self, membername, default)
            done = True
        elif excstr is not None:
            done = True
            raise Exception(excstr)

        if not done:
            setattr(self, membername, None)

class Blob(BaseVarType):
    _innertype = bytes
    _outertype = DbType.BLOB
    
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def to_innertype(self, dta):
        if dta is None:
            return None
        else:
            return bytes(dta)

class String(BaseVarType):
    _innertype = str
    _outertype = DbType.TEXT
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def to_innertype(self, dta):
        if dta is None:
            return None
        else:
            return str(dta)
        

class UUid(BaseVarType):
    _innertype = uuid.uuid4
    _outertype = DbType.TEXT

    def to_innertype(self, dta):
        if dta is None:
            return None
        t = type(dta)

        if t is uuid.uuid4:
            return dta
        elif t is str:
            return uuid.UUID(dta)
        else:
            raise Exception("Type <{0}> cannot be tranformed into a uuid".format(t.__name__))

class Int(BaseVarType):
    _innertype = int
    _outertype = DbType.INTEGER

    def to_innertype(self, dta):
        if dta is None:
            return None
        t = type(dta)

        if t is int:
            return dta
        elif t is str:
            return int(dta)
        else:
            raise Exception("Type <{0}> cannot be tranformed into an int".format(t.__name__))

class Float(BaseVarType):
    _innertype = float
    _outertype = DbType.REAL

    def to_innertype(self, dta):
        if dta is None:
            return None
        t = type(dta)

        if t is float:
            return dta
        elif t is str:
            return float(dta)
        else:
            raise Exception("Type <{0}> cannot be tranformed into a float".format(t.__name__))

class Boolean(BaseVarType):
    _innertype = bool
    _outertype = DbType.TEXT

    def to_innertype(self, dta):
        if dta is None:
            return None
        t = type(dta)

        if t is bool:
            return dta
        elif t is str:
            lowdta = dta.lower()
            if lowdta in ["ja", "yes", "wahr", "true", "y", "1"]:
                return True
            elif lowdta in ["nein", "no", "unwahr", "false", "n", "0"]:
                return False
            else:
                raise Exception("The string <{0}> cannot be transformed to a bool".format(dta))
        elif t is int:
            return dta == 1
        else:
            raise Exception("Type <{0}> cannot be tranformed into a bool".format(t.__name__))

class DateTime(BaseVarType):
    innertype = dt.datetime
    _outertype = DbType.TIMESTAMP

    def to_innertype(self, dta):
        if dta is None:
            return None
        t = type(dta)

        if t is dt.datetime:
            return dta
        elif t is str:
            return dt.strptime(dta, "%m.%d.%Y %H:%M:%S")
        else:
            raise Exception("Type <{0}> cannot be tranformed into a datetime".format(t.__name__))

class Catalog(BaseVarType):
    _innertype = str
    _outertype = DbType.TEXT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._getpara(kwargs, "catalogtype", excstr="catalogdefinition without catalogtype is not a valid catalog definition")

    def to_innertype(self, dta):
        raise Exception("do not use to_innertype in catalogs!")

    def get_catalogtype(self):
        return self._catalogtype

# classes for queries
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

# special data declarations

class _EmbeddedObject(BaseVarType):
    _innertype = object

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._getpara(kwargs, "targettype", excstr="EmbeddedObject needs a targettype!!")
        self._getpara(kwargs, "autofill", default=True)

    def is_dbstorable(self):
        #not directly storable in the database
        return False

    def get_targettype(self):
        return self._targettype

    def get_autofill(self) -> bool:
        return self._autofill

    def get_foreign_keyname(self):
        if type(self._foreignid) is str: return self._foreignid

        vname = getvarname(self._foreignid)

        if vname is not None: #if we managed to get the name, store it for future use (caching)
            self._foreignid = vname

        return vname

    def get_local_keyname(self):
        if type(self._localid) is str: return self._localid

        vname = getvarname(self._localid)

        if vname is not None: #if we managed to get the name, store it for future use (caching)
            self._localid = vname

        return vname

class _EmbeddedList(_EmbeddedObject):
    _innertype = list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class JoinedEmbeddedList(_EmbeddedList):
    _innertype = list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._getpara(kwargs, "localid", default="_id")
        self._getpara(kwargs, "foreignid", excstr="A JoinedEmbeddedList needs a foreign id!!!")
        self._getpara(kwargs, "autofill", default=False)
        self._getpara(kwargs, "cascadedelete", default=False)

    def get_cascadedelete(self):
        return self._cascadedelete



class IntersectedList(_EmbeddedList):
    _innertype = list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._getpara(kwargs, "autofill", default=False)
        self._getpara(kwargs, "cascadedelete", default=False)
        self._getpara(kwargs, "localid", default="_id") 
        self._getpara(kwargs, "foreignid", default="_id")
        self._getpara(kwargs, "interupid", default="upid") 
        self._getpara(kwargs, "interdownid", default="downid")

    def get_down_keyname(self):
        return self._interdownid

    def get_up_keyname(self):
        return self._interupid


class JoinedEmbeddedObject(_EmbeddedObject):
    _innertype = object

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._getpara(kwargs, "localid", excstr="A JoinedEmbeddedObject needs a local id which points to the joined object")
        self._getpara(kwargs, "foreignid", default="_id")
        self._getpara(kwargs, "cascadedelete", default=False)

    def get_cascadedelete(self):
        return self._cascadedelete

class ClassDictEntry(object):
    def __init__(self, membername, dectype, declaration):
        self._membername = membername
        self._dectype = dectype
        self._declaration = declaration

    def  get_default(self):
        return self._declaration.get_default()

    def get_dectype(self):
        return self._dectype

    def get_outertype(self):
        return self._declaration._outertype

    def get_declaration(self):
        return self._declaration

    def __repr__(self):
        return "datamember: {} dectype{} declared {}".format(self._membername, self._dectype, self._declaration)

class PBase(object):
    """Base class for any persistant class
       Derive from this and your class will be persistent"""
    _classdict = {}
    Id = UUid()
    Created = DateTime()
    LastUpdate = DateTime()

    @classmethod
    def _setup_class_dict(cls):

        if cls in cls._classdict.keys(): return

        classmemberdict = {}
        allclasses = inspect.getmro(cls) # get classes in method call order aka top derived class first
        for allclass in allclasses:
            if issubclass(allclass, PBase):
                members = vars(allclass)
                for key, value in members.items():
                    if key[0].isupper() and issubclass(value.__class__, BaseVarType):
                        if key=="Id":
                            mykey = "_id"
                        else:
                            mykey = key.lower()

                        if not mykey in classmemberdict.keys(): # do not overwrite overridden member infos
                            classmemberdict[mykey] = ClassDictEntry(key, type(value), getattr(allclass, key))
        
        cls._classdict[cls] = classmemberdict

    @classmethod
    def _getclstablename(cls):
        return cls.get_collection_name().lower()

    @classmethod
    def get_collection_name(cls):
        if hasattr(cls, "_collectionname"):
            return getattr(cls, "_collectionname")
        else:
            return cls.__name__

    @classmethod
    def get_memberdeclarationforcls(cls, membercls, membername : str):
        """return then memberdeclaration for a member of the given class"""
        cd = cls._classdict[membercls]
        md = cd[membername]
        return md.get_declaration()

    @classmethod
    def get_clsdict(cls):
        """return the classdict for the class"""
        return cls._classdict[cls]

    @classmethod
    def is_catalogmember(cls, membername):
        cd = cls._classdict[cls]
        md = cd[membername]
        decl = md.get_declaration()
        return issubclass(type(decl), Catalog)

    @classmethod
    def additional_where(cls):
        """ adds an additional whereclause to every where for this class
            override to add your own additional where for your derived class
            mybe like: MyCls.MyProp=="something" """
        return None

    def clone(self):
        """ create an intelligent clone by deep copying all of the members which are declared
            as persistent. _id is not omitted!
        """

        cls = self.__class__
        answ = cls()
        decls = cls.get_clsdict()
        for mname, mdecl in decls.items():
            val = getattr(self, mname, None)
            if val is None:
                setattr(answ, mname, val)
            else:
                if mdecl._dectype is JoinedEmbeddedObject:
                    setattr(answ, mname, val.clone())
                elif mdecl._dectype is IntersectedList:
                    answval = []
                    for valelm in val:
                        answval.append(valelm.clone())
                    setattr(answ, mname, answval)
                elif mdecl._dectype is JoinedEmbeddedList:
                    answval = []
                    for valelm in val:
                        answval.append(valelm.clone())
                    setattr(answ, mname, answval)
                    
                else:
                    setattr(answ, mname, val)

        return answ

    def __init__(self, **kwargs):
        self._valuesdict = {}
        self.__class__._setup_class_dict()
        for key, value in kwargs.items():
            self._set_my_attribute(key, value)
        self.initialise_attributes()
        self._dbvaluescache = None

    def has_changed(self):
        if self._dbvaluescache is None: #no read from db occured before we ask this
            return True

        vd = self._get_my_memberdict()
        for key, value in vd.items():
            if hasattr(self, key):
                membval = getattr(self, key)
                if not key in self._dbvaluescache:
                    continue #we rely on the correct preparation of the cache
                    #all joined types are not compared for changes

                if self._dbvaluescache[key] != membval:
                    return True

        return False
        

    def initialise_attributes(self):
        vd = self._get_my_memberdict()
        for key, value in vd.items():
            if hasattr(self, key) and getattr(self, key) is not None:
                continue
            
            setattr(self, key, value.get_default())

    def _set_my_attribute(self, key, value):
        """ set my own attributes in a controlled manner
        """
        mycld = self._get_my_memberdict()
        if key not in mycld.keys():
            raise Exception("Cannot initialise undefined member {}".format(key))

        setattr(self, key, value)
        
    def _get_my_memberdict(self):
        mycls = self.__class__
        return mycls._classdict[mycls]

    def get_memberdeclaration(self, membername):
        md = self._get_my_memberdict()[membername]
        return md.get_declaration()


class PCatalog(PBase):
    """Basic class for Attributes defining a catalog"""
    _collectionname = "catalog"
    _cattype = None #overriden in each catalog derived from this class
    _langsensitive = False # by default no language sensititivity, bur may be overriden by derived catalogs
    Type = String(uniquegrp="_CAT_UNI_01")
    Code = String(uniquegrp="_CAT_UNI_01")
    Value = String()
    LangCode = String(uniquegrp="_CAT_UNI_01")

    def __str__(self):
        return "{}.{}.{}.{}".format(self.type, self.langcode, self.code, self.value)
        
    def __eq__(self, other):
        if other is None:
            return False
            
        return self.langcode==other.langcode and self.type==other.type and self.code == other.code
        
    @classmethod
    def is_langsensitive(cls):
        return cls._langsensitive

    @classmethod
    def additional_where(cls):
        if cls._cattype is not None:
            return cls.Type == cls._cattype #this adds where type=<myclastype> to any call 
        else:
            return None

class CommonInter(PBase):
    """derivew from this if you want to have all your intersections reside in just one
    collection identified by a type str"""
    _collectionname = "commoninter"
    _intertype = None  #override in your derived class to distinguish your intersection from all of the others
    UpId = UUid(uniquegrp="_COMN_INTER_UNI")
    DownId = UUid(uniquegrp="_COMN_INTER_UNI")
    InterType = String(uniquegrp="_COMN_INTER_UNI")

    @classmethod
    def additional_where(cls):
        if cls._intertype is not None:
            return cls.InterType == cls._intertype #this adds where type=<myintertype> to any call of where
        else:
            return None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.intertype=self.__class__._intertype

def getvarname(decl: BaseVarType):
    """get the name used for a field of a declaration 

       search is done by _varcode which every intstance of a field declaration gets automatically
    """
    for cls, cldentry in PBase._classdict.items():
        for key, value in cldentry.items():
            if value._declaration._varcode == decl._varcode: 
                return key
    return None

def getsubedvarname(decl: BaseVarType):
    """get the varname with dots when subnames are given or simply like getvarname when there are no subs
    """

    if decl._subdef is None:
        return getvarname(decl)
    else:
        return getvarname(decl) + "." + getsubedvarname(decl._subdef)

def is_none_or_empty(tstr : str) -> bool:
    """checks a string for None or emptyness
    returns True when tstr is None or a string which contains no characters at all"""
    return tstr is None or len(tstr)==0
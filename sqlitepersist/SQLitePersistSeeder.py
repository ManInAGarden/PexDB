import importlib
import json

from .SQLitePersistBasicClasses import *
from .SQLitePersistFactoryParts import *
from .SQLitePersistQueryParts import *


class SQPSeeder(object):
    def __init__(self, fact, filepath) -> None:
        self._filepath = filepath
        self._fact = fact
        super().__init__()

    def create_seeddata(self):
        with open(self._filepath, 'r', encoding="utf8") as f:
            data = json.load(f)
        
        for datk, datlist in data.items():
            cls = self._getclass(datk)
            for datmap in datlist:
                dm = self._doreplacements(cls, datmap)
                s = cls(**dm)
                self._fact.flush(s)

    def _doreplacements(self, targetcls, datmap):
        dm = dict()
        
        for datkey, datvalue in datmap.items():
            if type(datvalue) is str and datvalue.startswith("${"):
                dav = self._replace(datvalue)
            elif targetcls.is_catalogmember(datkey):
                dav = self._get_catalog(targetcls, datkey, datvalue)
            else:
                dav = datvalue

            dm[datkey] = dav

        return dm

    def _replace(self, dav):
        answ = ""

        definition = dav.replace("${", "").replace("}","")
        defparts = definition.split(":")

        if defparts is None or len(defparts) != 3:
            raise Exception("Seed data error in " + dav)

        searchname = defparts[0]
        srchvalue = defparts[1]
        getfieldname = defparts[2]

        lidx = searchname.rfind(".")
        if lidx < 0:
            raise Exception("Seed data error in {0}. No point found in definition to seperate field from class".format(dav))
        
        searchclassname = searchname[:lidx]
        searchfielddefinname = searchname[lidx+1:]

        cls = self._getclass(searchclassname)
        fielddecl = PBase.get_memberdeclarationforcls(cls, searchfielddefinname)
        q = SQQuery(self._fact, cls).where(fielddecl == srchvalue)
        ct = 0
        firstf = None
        for fobj in q:
            ct += 1
            firstf = fobj

        if ct != 1:
            raise Exception("object not found or not unique in search of {0}.{1} = {2}".format(searchclassname, searchfielddefinname, str(srchvalue)))

        answ = firstf.__getattribute__(getfieldname)
        return answ

    def _getclass(self, clsname : str):
        if clsname is None or len(clsname)==0:
            raise Exception("Mocker._getclass(classname) for an empty classname is not a valid call")

        lastdot = clsname.rindex('.')
        modulename = clsname[0:lastdot]
        clsname = clsname[lastdot + 1::]
        module = importlib.import_module(modulename)
        return getattr(module, clsname)

    def _get_catalog(self, targetcls, targetmember, codekey):
        """get a real catalog value for the given key"""
        if "#" in codekey:
            parts = codekey.split("#")
            if len(parts) != 2:
                raise Exception("Codekey for catalog search contains more then one # in <{0}>. Use only a single # to separate langeuage from key like ENU#SOME_KEY.".format(codekey))
            lang = parts[0]
            code = parts[1]
        else:
            lang = None
            code = codekey
        
        membdec = PBase.get_memberdeclarationforcls(targetcls, targetmember)
        catacls = membdec.get_catalogtype()
        answ = self._fact.getcat(catacls, code, lang)

        if answ is None:
            raise Exception("Catalog value for class <{0}> not found for seed-key <{1}> in seeding for class <{2}>".format(str(catacls), codekey, str(targetcls)))

        return answ
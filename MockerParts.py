import importlib
import json
import datetime
import sqlitepersist as sqp
from PersistClasses import *

class Mocker(object):
   
    def __init__(self, fact : sqp.SQFactory) -> None:
        self._sqpf = fact

    def create_seeddata(self, filepath):
        # self._mpf._db.drop_collection(MrMsCat.get_collection_name()) #this drops all of the catalogs becaus they are all in the same collection!
        seeder = Seeder(self._sqpf, filepath)
        seeder.create_seeddata()

    def create_printer(self, producedby="Qidi tech", name="X-MAX", abbreviation="QXMX", firmware="MARLIN", version="1.1.3", yearofbuild=2020, monthofbuild=9):
        pr = Printer(producedby=producedby, name=name, abbreviation=abbreviation, firmware=firmware, yearofbuild=yearofbuild, monthofbuild=monthofbuild)
        self._sqpf.flush(pr)
        return pr

    def create_extruder(self, producedby="QIDI", name="HighTemp", abbreviation="QIDIXPHTAM", maxtemperature=300, hascooler=False):
        ext = Extruder(producedby=producedby, 
            name=name, 
            abbreviation = abbreviation, 
            maxtemperature=maxtemperature, 
            hascooler=hascooler)
        self._sqpf.flush(ext)
        return ext

    def create_setting(self, parameterid=None, value=0.0):
        setg = Setting(parameterid=parameterid, value=value)
        self._sqpf.flush(setg)
        return setg

    def create_experiment(self, carriedoutdt = None, description="unit-test experiment"):
        if carriedoutdt is None:
            cod = datetime.datetime.now()
        else:
            cod = carriedoutdt

        allparasq = sqp.SQQuery(self._sqpf, Parameter) #get all parameter definitions
        for para in allparasq:
            setg = self.create_setting(parameterid=para._id, value=10.0)

        exp = Experiment(carriedoutdt=cod, description=description)
        self._sqpf.flush(exp)

    
class Seeder(object):
    def __init__(self, fact, filepath) -> None:
        self._filepath = filepath
        self._fact = fact
        super().__init__()

    def create_seeddata(self):
        with open(self._filepath, 'r', encoding="utf8") as f:
            data = json.load(f)
        
        for datk, datlist in data.items():
            cls = self._getclass(datk)
            colname = cls.get_collection_name()
            for datmap in datlist:
                dm = self._doreplacements(datmap)
                s = cls(**dm)
                self._fact.flush(s)

    def _doreplacements(self, datmap):
        dm = dict()
        
        for datkey, datvalue in datmap.items():
            if type(datvalue) is str and datvalue.startswith("${"):
                dav = self._replace(datvalue)
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
        fielddecl = sqp.PBase.get_memberdeclarationforcls(cls, searchfielddefinname)
        q = sqp.SQQuery(self._fact, cls).where(fielddecl == srchvalue)
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


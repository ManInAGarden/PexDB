import importlib
import json
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
                s = cls(**datmap)
                self._fact.flush(s)

    def _getclass(self, clsname : str):
        if clsname is None or len(clsname)==0:
            raise Exception("Mocker._getclass(classname) for an empty classname is not a valid call")

        lastdot = clsname.rindex('.')
        modulename = clsname[0:lastdot]
        clsname = clsname[lastdot + 1::]
        module = importlib.import_module(modulename)
        return getattr(module, clsname)


import datetime
import sqlitepersist as sqp
from PersistClasses import *

class Mocker(object):
   
    def __init__(self, fact : sqp.SQFactory) -> None:
        self._sqpf = fact

    def create_seeddata(self, filepath):
        # self._mpf._db.drop_collection(MrMsCat.get_collection_name()) #this drops all of the catalogs becaus they are all in the same collection!
        seeder = sqp.SQPSeeder(self._sqpf, filepath)
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

    def create_setting(self, parameterid=None, value=0.0, experimentid=None):
        setg = Setting(parameterid=parameterid, value=value, experimentid=experimentid)
        self._sqpf.flush(setg)
        return setg

    def create_experiment(self, carriedoutdt = None, description="unit-test experiment"):
        if carriedoutdt is None:
            cod = datetime.datetime.now()
        else:
            cod = carriedoutdt

        prin = self.create_printer(name="X-TEST", abbreviation="QXTST")
        extr = self.create_extruder()
        exp = Experiment(carriedoutdt=cod, 
            description=description, 
            extruderusedid=extr._id, 
            printerusedid=prin._id)
            
        self._sqpf.flush(exp)
        exp.settings = []
        allparasq = sqp.SQQuery(self._sqpf, Parameter) #get all parameter definitions
        for para in allparasq:
            setg = self.create_setting(parameterid=para._id, value=10.0, experimentid=exp._id)
            exp.settings.append(setg)

        return exp

       

    

import datetime
import uuid
import sqlitepersist as sqp
from PersistClasses import *
from sqlitepersist.SQLitePersistQueryParts import SQQuery
import creators as cr

class Mocker(object):
   
    def __init__(self, fact : sqp.SQFactory) -> None:
        self._sqpf = fact

    def create_seeddata(self, filepath):
        # self._mpf._db.drop_collection(MrMsCat.get_collection_name()) #this drops all of the catalogs becaus they are all in the same collection!
        seeder = sqp.SQPSeeder(self._sqpf, filepath)
        seeder.create_seeddata()

    def create_project(self, name="tstproj", statcode="INIT"):
        proj = Project(name=name, status = self._sqpf.getcat(ProjectStatusCat, statcode))
        self._sqpf.flush(proj)
        return proj

    def _create_ref_dict(self, sq : SQQuery) -> dict:
        lst = list(sq)
        answ = {}
        for el in lst:
            answ[el.abbreviation] = el

        return answ

    def add_response_preps(self, proj : Project, resps : dict):
        assert proj is not None
        assert len(resps) > 0
        assert proj._id is not None

        rdefs_dict = self._create_ref_dict(SQQuery(self._sqpf, ResponseDefinition))

        for rabr, respdta in resps.items():
            rdef = rdefs_dict[rabr]
            rprep = ProjectResponsePreparation(projectid = proj._id,
                responsedefinition = rdef,
                responsedefinitionid = rdef._id,
                combinationweight = respdta[0])

            self._sqpf.flush(rprep)

    def add_factor_preps(self, proj : Project, factlevels : dict):
        assert proj is not None
        assert len(factlevels) > 0
        assert proj._id is not None

        #get all fdefs
        fdef_dict = self._create_ref_dict(SQQuery(self._sqpf, FactorDefinition))

        for fabbr, prepdef in factlevels.items():
            fdef = fdef_dict[fabbr]
            fprep = ProjectFactorPreparation(projectid = proj._id, 
                factordefinition = fdef,
                factordefinitionid = fdef._id,
                minvalue=prepdef[0], 
                maxvalue=prepdef[1], 
                levelnum=prepdef[2])

            self._sqpf.flush(fprep)

    def create_printer(self, producedby="Qidi tech", name="X-MAX", abbreviation=None, firmware="MARLIN", version="1.1.3", yearofbuild=2020, monthofbuild=9):
        if abbreviation is None:
            abr = self.getuniqueabbrev("PRN")
        else:
            abr = abbreviation

        pr = Printer(producedby=producedby, name=name, abbreviation=abr, firmware=firmware, yearofbuild=yearofbuild, monthofbuild=monthofbuild)
        self._sqpf.flush(pr)
        return pr

    def create_extruder(self, producedby="QIDI", name="HighTemp", abbreviation=None, maxtemperature=300, hascooler=False):
        if abbreviation is None:
            abr = self.getuniqueabbrev("EXT")
        else:
            abr = abbreviation

        ext = Extruder(producedby=producedby, 
            name=name, 
            abbreviation = abr, 
            maxtemperature=maxtemperature, 
            hascooler=hascooler)
        self._sqpf.flush(ext)
        return ext

    def create_factor(self, factdefid=None, value=0.0, experimentid=None, factdef=None):
        setg = FactorValue(factordefinitionid=factdefid, 
            value=value, 
            experimentid=experimentid, 
            factordefinition=factdef)
        self._sqpf.flush(setg)
        return setg

    def getuniqueabbrev(self, leader):
        uidh = uuid.uuid4().hex
        return leader + "_" + uidh

    def create_experiment(self, carriedoutdt = None, description="unit-test experiment"):
        if carriedoutdt is None:
            cod = datetime.datetime.now()
        else:
            cod = carriedoutdt

        prin = self.create_printer(name="X-TEST")
        extr = self.create_extruder()
        exp = Experiment(carriedoutdt=cod, 
            description=description, 
            extruderusedid=extr._id, 
            printerusedid=prin._id)
            
        self._sqpf.flush(exp)
        exp.factors = []
        allparasq = sqp.SQQuery(self._sqpf, FactorDefinition) #get all parameter definitions
        for para in allparasq:
            setg = self.create_factor(factdefid=para._id, value=10.0, experimentid=exp._id, factdef=para)
            exp.factors.append(setg)

        return exp

    def create_fullfactorial_experiments(self, 
            fpreps, 
            rpreps,
            kind = cr.CreaSequenceEnum.LINEAR,
            projectname="linregproj",
            docentre = False):
        """ create all experiments by a full factorial scheme
        """
        
        prin = self.create_printer(name="LIN_SIMPLE_PRINTER")
        extr = self.create_extruder(name="LIN_SIMPLE_EXTRUDER")
        proj = self.create_project(name=projectname)

        self.add_factor_preps(proj, fpreps)
        self.add_response_preps(proj, rpreps)

        crea = cr.CreaFullFactorial(self._sqpf, proj,
            prin,
            extr,
            kind,
            docentre=docentre)

        cnum = crea.create()

        return cnum, proj
        
       

    

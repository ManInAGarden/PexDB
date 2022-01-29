import datetime
import uuid
import sqlitepersist as sqp
from PersistClasses import *
from sqlitepersist.SQLitePersistQueryParts import SQQuery
import creators as cr

class Mocker(object):
   
    def __init__(self, fact : sqp.SQFactory) -> None:
        self._sqpf = fact
        self._fdef_cache = None

    @property
    def fdef_dict(self):
        if self._fdef_cache is None:
            self._fdef_cache = self._create_ref_dict(SQQuery(self._sqpf, FactorDefinition))

        return self._fdef_cache

    def create_seeddata(self, filepath):
        # self._mpf._db.drop_collection(MrMsCat.get_collection_name()) #this drops all of the catalogs becaus they are all in the same collection!
        seeder = sqp.SQPSeeder(self._sqpf, filepath)
        seeder.create_seeddata()

    def create_project(self, name="tstproj", statcode="INIT"):
        proj = Project(name=name, status = self._sqpf.getcat(ProjectStatusCat, statcode))
        self._sqpf.flush(proj)
        return proj

    def _create_ref_dict(self, sq : SQQuery) -> dict:
        answ = {}
        for el in sq:
            answ[el.abbreviation] = el

        return answ

    def add_response_preps(self, proj : Project, resps : dict):
        assert proj is not None
        assert len(resps) > 0
        assert proj._id is not None

        rdefs_dict = self._create_ref_dict(SQQuery(self._sqpf, ResponseDefinition))

        for rabr, valdict in resps.items():
            fdef = rdefs_dict[rabr] #get the factor definition to be used for the project-factor-preparation
            fprep = self.rprep_from_valdict(proj, valdict, fdef)


    def add_enviro_preps(self, proj : Project, envs : dict):
        assert proj is not None
        assert len(envs) > 0
        assert proj._id is not None

        edefs_dict = self._create_ref_dict(SQQuery(self._sqpf, EnviroDefinition))

        for eabr, envpdta in envs.items():
            edef = edefs_dict[eabr]
            eprep = ProjectEnviroPreparation(projectid = proj._id,
                envirodefinition = edef,
                envirodefinitionid = edef._id)

            self._sqpf.flush(eprep)

    def rprep_from_valdict(self, proj : Project, vdict:dict, fdef : ResponseDefinition):
        rprep = ProjectResponsePreparation(projectid = proj._id, 
                responsedefinition = fdef,
                responsedefinitionid = fdef._id,
                combinationweight = self._get_float(vdict, "combinationweight"))

        self._sqpf.flush(rprep)

    def fprep_from_valdict(self, proj : Project, vdict:dict, fdef : FactorDefinition):
        fprep = ProjectFactorPreparation(projectid = proj._id, 
                factordefinition = fdef,
                factordefinitionid = fdef._id,
                minvalue=vdict["minvalue"], 
                maxvalue=vdict["maxvalue"], 
                levelnum=self._get_int(vdict, "levelnum", 2),
                iscombined=self._get_bool(vdict, "iscombined"),
                isnegated=self._get_bool(vdict, "isnegated"))

        self._sqpf.flush(fprep)
        if fprep.iscombined:
            if not "factorcombidefs" in vdict:
                raise Exception("iscombined==True bur no combinations found in mocking of factor {}".format(fdef.abbreviation))

            combidefs = vdict["factorcombidefs"]
            assert type(combidefs) is list

            for fabbr in combidefs:
                factdef = self.fdef_dict[fabbr]
                inter = FactorCombiDefInter(upid=fprep._id, 
                    downid=factdef._id)

                self._sqpf.flush(inter)
                inter.factordeinition = fdef

                if fprep.factorcombidefs is None:
                    fprep.factorcombidefs = []
                fprep.factorcombidefs.append(inter)

        return fprep

    def add_factor_preps(self, proj : Project, factlevels : dict):
        assert proj is not None
        assert len(factlevels) > 0
        assert proj._id is not None

        for fabbr, valdict in factlevels.items():
            fdef = self.fdef_dict[fabbr] #get the factor definition to be used for the project-factor-preparation
            fprep = self.fprep_from_valdict(proj, valdict, fdef)

    def _get_bool(self, valdict, key,  default=False):
        if key not in valdict:
            return default
        else:
            return valdict[key]

    def _get_int(self, valdict, key, default=0):
        if key not in valdict:
            return default
        else:
            return valdict[key]

    def _get_float(self, valdict, key, default=0.0):
        if key not in valdict:
            return default
        else:
            return valdict[key]

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

    def create_fractfactorial_experiments(self, 
            fpreps, 
            rpreps,
            epreps = None,
            kind = cr.CreaSequenceEnum.LINEAR,
            projectname="linregproj",
            docentre = False):
        """ create all experiments by a fractional factorial scheme
            where combined factors are defined in the projectfactorpreparations
        """
        
        prin = self.create_printer(name="LIN_SIMPLE_PRINTER")
        extr = self.create_extruder(name="LIN_SIMPLE_EXTRUDER")
        proj = self.create_project(name=projectname)

        self.add_factor_preps(proj, fpreps)
        self.add_response_preps(proj, rpreps)
        if epreps is not None:
            self.add_enviro_preps(proj, epreps)

        crea = cr.CreaFractFactorial(self._sqpf, proj,
            prin,
            extr,
            kind,
            docentre=docentre)

        cnum = crea.create()

        return cnum, proj
        
       

    

import csv
from gettext import Catalog
import json
import importlib
from time import strptime
from typing import Any
from uuid import UUID, uuid4

from numpy import full, isin
import sqlitepersist as sqp
from PersistClasses import *
from sqlitepersist.SQLitePersistBasicClasses import DateTime, PBase, PCatalog

class PexJSONEncoder(json.JSONEncoder):
    """ custom encoder for json exports of complete projects
    """
    def encode_pbase(self, obj):
        ot = type(obj)
        full_clsname = ot.__module__ + "." + ot.__name__
        answdict = {"_clsname_":full_clsname}
        mdict = obj._get_my_memberdict()
        for membname, membinfo in mdict.items():
            answdict[membname] = getattr(obj, membname)

        return answdict


    def default(self, obj: Any) -> Any:
        if isinstance(obj, PCatalog):
            return obj.code
        elif isinstance(obj, sqp.PBase):
            return self.encode_pbase(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y%m%dT%H:%M:%S")
        elif isinstance(obj, UUID):
            return obj.hex
        else:
            return super().default(obj)
        
class ProjectImporter:
    def __init__(self, fact : sqp.SQFactory, proj : Project, printer=None, extruder=None):
        self._dbfact = fact
        self._p = proj
        self._extr = extruder
        self._pri = printer

    def _get_valob_fact(self, exp : Experiment, val : float, prep : ProjectFactorPreparation) :
        return FactorValue(experimentid=exp._id,
            value = val,
            factordefinition = prep.factordefinition,
            factordefinitionid = prep.factordefinitionid)

    def _get_valob_resp(self, exp : Experiment, val : float, prep : ProjectResponsePreparation) :
        return ResponseValue(experimentid=exp._id,
            value = val,
            responsedefinition = prep.responsedefinition,
            responsedefinitionid = prep.responsedefinitionid)


    def _get_valob_env(self, exp : Experiment, val : float, prep : ProjectEnviroPreparation) :
        return EnviroValue(experimentid=exp._id,
            value = val,
            envirodefinition = prep.envirodefinition,
            envirodefinitionid = prep.envirodefinitionid)

    def import_from_csv(self, filename):
        """ import all experiments from csv to a given and empty project
        """
        dbf = self._dbfact
        pr = self._p
        f_preps = sqp.SQQuery(dbf, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId == pr._id).as_list()
        r_preps =sqp.SQQuery(dbf, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId == pr._id).as_list()
        e_preps = sqp.SQQuery(dbf, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==pr._id).as_list()
        
        #create a handy dict to map column headings
        coln_dict = {}
        for fp in f_preps:
            coln_dict[fp.factordefinition.abbreviation] = fp

        for rp in r_preps:
            coln_dict[rp.responsedefinition.abbreviation] = rp

        for ep in e_preps:
            coln_dict[ep.envirodefinition.abbreviation] = ep

        #now we know what to expect in the file which must at least contain data for what is definied/prepared
        #for the project

        with open(filename, mode="r", encoding="UTF-8", newline="\n") as f:
            csvr = csv.DictReader(f)
            ct = 0
            self._dbfact.begin_transaction()
            try:
                for row in csvr:
                    currexp = Experiment(projectid=self._p._id,
                        sequence = row["EXP_SEQUENCE"],
                        repnum = row["EXP_REPNUM"],
                        description=row["EXP_DESCRIPTION"],
                        extruderused=self._extr,
                        printerused = self._pri)

                    self._dbfact.flush(currexp)
                    currexp.factors = []
                    currexp.responses = []
                    currexp.enviros = []
                    ct += 1
                    for coln, cdta in coln_dict.items():
                        ctype = type(cdta)
                        if ctype == ProjectFactorPreparation:
                            valob = self._get_valob_fact(currexp, row[coln], cdta)
                            currexp.factors.append(valob)
                        elif ctype is ProjectResponsePreparation:
                            valob = self._get_valob_resp(currexp, row[coln], cdta)
                            currexp.responses.append(valob)
                        elif ctype is ProjectEnviroPreparation:
                            valob = self._get_valob_env(currexp, row[coln], cdta)
                            currexp.enviros.append(valob)
                        else:
                            raise NotImplemented("Unknown type in coldict!")

                        self._dbfact.flush(valob)

                self._dbfact.commit_transaction()
            except Exception as exc:
                self._dbfact.rollback_transaction()
                raise exc

    def import_from_json(self, filename):
        dechook = PexDecoderHook()

        with open(filename, mode="rt", encoding="UTF-8") as fp:
            jsonlst = json.load(fp, object_hook=dechook.pex_hook)
        
        #now we got all the object but nothing is stored in the db up to this point
        #we need a dict of old vs new ids and a dict of any already stored object first

        self._dbfact.begin_transaction()

        try:
            for jobj in jsonlst:
                if isinstance(jobj, PBase):
                    self._first_flush(jobj, dechook)
                else:
                    raise Exception("Non persistent object found on first level of imported objects")

            self._dbfact.commit_transaction()
        except Exception as exc:
            self._dbfact.rollback_transaction()
            raise exc

    def _first_flush(self, obj, dh):
        """ flush the objects of the lowest level of reference when they are not already present in the db
        """

        presobj = self._try_get_from_db(obj)
        if presobj is not None:
            dh._id_dict[obj._id] = presobj._id
        else:
            self._dbfact.flush(obj)
            dh._id_dict[obj._id] = obj._id

    def _try_get_from_db(self, obj):
        if isinstance(obj, Catalog):
            return None
        elif isinstance(obj, FactorDefinition):
            return sqp.SQQuery(self._dbfact, FactorDefinition).where(FactorDefinition.Abbreviation==obj.abbreviation).first_or_default(None)
        elif isinstance(obj, ResponseDefinition):
            return sqp.SQQuery(self._dbfact, ResponseDefinition).where(ResponseDefinition.Abbreviation==obj.abbreviation).first_or_default(None)        
        elif isinstance(obj, EnviroDefinition):
            return sqp.SQQuery(self._dbfact, EnviroDefinition).where(EnviroDefinition.Abbreviation==obj.abbreviation).first_or_default(None)        
        else:
            raise Exception("Unhandled type {} in _try_get_from_db".format(str(type(obj))))

class PexDecoderHook:

    def __init__(self):
        self._id_dict = {} #initialise a dict {<oldid>:<newid>}

    def _trfrm_uuid(self, val : str) -> UUID:
        if val is None or len(val)==0:
            return None

        id = UUID(val)
        self._id_dict[id] = None

        return id

    def _trfrm_datetime(self, val : str) -> datetime:
        if val is None or len(val)==0:
            return None

        return datetime.strptime(val, "%Y%m%dT%H:%M:%S")

    def _getclass(self, full_clsname : str):
        if full_clsname is None or len(full_clsname)==0:
            raise Exception("ExportImportProjects._getclass(classname) for an empty classname is not a valid call")

        lastdot = full_clsname.rindex('.')
        modulename = full_clsname[0:lastdot]
        full_clsname = full_clsname[lastdot + 1::]
        module = importlib.import_module(modulename)
        return getattr(module, full_clsname)


    def _set_pexattr(self, obj, mn, dect, dct):
        if mn not in dct:
            value = None
        else:
            value = dct[mn]
            dtype = dect._dectype
            if dtype is UUid:
                value = self._trfrm_uuid(value)
            elif dtype is DateTime:
                value = self._trfrm_datetime(value)

        setattr(obj, mn, value)

    def _get_pexinst(self, dct):
        full_clsname = dct["_clsname_"]
        cls = self._getclass(full_clsname)
        if not issubclass(cls, sqp.PBase):
            raise Exception("Class {} is not a persistent sqlite class. Must be derived from PBase!".format(full_clsname))
        
        obj = cls()
        mdict = obj._get_my_memberdict()
        for membname, membinfo in mdict.items():
            self._set_pexattr(obj, membname, membinfo, dct)

        return obj

    def pex_hook(self, dct):
        if "_clsname_" in dct:
            return self._get_pexinst(dct)
        else:
            return dct

class ProjectExporter:
    def __init__(self, fact : sqp.SQFactory, proj : Project):
        self._fact = fact
        self._p = proj 

    def export_to_csv(self, filename):
        """ export the experiments to a csv for external use during the experiments and othe rpurposes
        """
        header = ["EXP_SEQUENCE", "EXP_REPNUM", "EXP_DESCRIPTION"]
        exp_q = sqp.SQQuery(self._fact, Experiment).where(Experiment.ProjectId==self._p._id)
        experiments = list(exp_q)
        if len(experiments) <= 0:
            raise Exception("No experiments are defined in the given project, nothing will be exported")

        fprep_q = sqp.SQQuery(self._fact, 
            ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._p._id)
        fpreps = list(fprep_q)
        rprep_q = sqp.SQQuery(self._fact, 
            ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._p._id)
        rpreps = list(rprep_q)
        eprep_q = sqp.SQQuery(self._fact, 
            ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==self._p._id)
        epreps = list(eprep_q)

        for fprep in fpreps:
            fdef = fprep.factordefinition
            head = fdef.abbreviation
            # if fdef.unit is not None:
            #     head += "[{}]".format(fdef.unit.abbreviation)

            header.append(head)

        for rprep in rpreps:
            fdef = rprep.responsedefinition
            head = fdef.abbreviation
            # if fdef.unit is not None:
            #     head += "[{}]".format(fdef.unit.abbreviation)

            header.append(head)

        for eprep in epreps:
            fdef = eprep.envirodefinition
            head = fdef.abbreviation
            # if fdef.unit is not None:
            #     head += "[{}]".format(fdef.unit.abbreviation)

            header.append(head)

        with open(filename, mode="w", encoding="UTF-8", newline="\n") as f:
            cwr = csv.writer(f)
            cwr.writerow(header)

            for exp in experiments:
                self._fact.fill_joins(exp, 
                    Experiment.Factors,
                    Experiment.Responses,
                    Experiment.Enviros)

                data = []
                data.append(exp.sequence)
                data.append(exp.repnum)
                data.append(exp.description)
                for fv in exp.factors:
                    data.append(fv.value)
                for rv in exp.responses:
                    data.append(rv.value)
                for ev in exp.enviros:
                    data.append(ev.value)

                cwr.writerow(data)

    def export_to_json(self, 
        filename : str, 
        include_preps : bool = True, 
        includedefs : bool = True):
        """ export a complete project in json
            main purpose is to import it again later on or into another system
        """
        exports = []
        if includedefs:
            fdefs_q = sqp.SQQuery(self._fact, FactorDefinition)
            rdefs_q = sqp.SQQuery(self._fact, ResponseDefinition)
            edefs_q = sqp.SQQuery(self._fact, EnviroDefinition)
            printers_q = sqp.SQQuery(self._fact, Printer)
            extruders_q = sqp.SQQuery(self._fact, Extruder)
            exports.extend(fdefs_q)
            exports.extend(rdefs_q)
            exports.extend(edefs_q)
            exports.extend(printers_q)
            exports.extend(extruders_q)

        exp_q = sqp.SQQuery(self._fact, Experiment).where(Experiment.ProjectId==self._p._id)
        experiments = list(exp_q)
        if len(experiments) <= 0:
            raise Exception("No experiments are defined in the given project, nothing will be exported")

        exports.append(self._p)
        for exp in experiments:
            self._fact.fill_joins(exp, 
                Experiment.Factors, 
                Experiment.Responses, 
                Experiment.Enviros)
            exports.append(exp)

        if include_preps:
            fpreps = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._p._id).as_list()
            exports.extend(fpreps)
            rpreps = sqp.SQQuery(self._fact, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._p._id).as_list()
            exports.extend(rpreps)
            epreps = sqp.SQQuery(self._fact, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==self._p._id).as_list()
            exports.extend(epreps)

        with open(filename, mode="wt", encoding="UTF-8") as f:
            json.dump(exports, f, cls=PexJSONEncoder, indent=4)


import csv

import sqlitepersist as sqp
from PersistClasses import *

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
        
        #create a handy dict to map clumn headings
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

class ProjectExporter:
    def __init__(self, fact : sqp.SQFactory, proj : Project):
        self._fact = fact
        self._p = proj

    def export_to_csv(self, filename):
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
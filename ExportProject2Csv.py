import csv

import sqlitepersist as sqp
from PersistClasses import *

class Project2CsvExporter:
    def __init__(self, fact : sqp.SQFactory, proj : Project, experiments : list):
        self._fact = fact
        self._p = proj
        self._exps = experiments

    def export(self, filename):
        header = ["experiment"]
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
            head = fdef.name
            if fdef.unit is not None:
                head += "[{}]".format(fdef.unit.abbreviation)

            header.append(head)

        for rprep in rpreps:
            fdef = rprep.responsedefinition
            head = fdef.name
            if fdef.unit is not None:
                head += "[{}]".format(fdef.unit.abbreviation)

            header.append(head)

        for eprep in epreps:
            fdef = eprep.envirodefinition
            head = fdef.name
            if fdef.unit is not None:
                head += "[{}]".format(fdef.unit.abbreviation)

            header.append(head)

        with open(filename, mode="w", encoding="UTF-8", newline="\n") as f:
            cwr = csv.writer(f)
            cwr.writerow(header)

            for exp in self._exps:
                data = []
                data.append(exp.description)
                for fv in exp.factors:
                    data.append(fv.value)
                for rv in exp.responses:
                    data.append(rv.value)
                for ev in exp.enviros:
                    data.append(ev.value)

                cwr.writerow(data)
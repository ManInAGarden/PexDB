import sqlitepersist as sqp
from .CreaBasics import _CreaBase
from PersistClasses import *

class CreaSingle(_CreaBase):
    def __init__(self, fact: sqp.SQFactory, project: Project, printer: Printer, extruder: Extruder):
        super().__init__(fact, project, printer, extruder)

    def create(self):
        """create a new single experiment"""

        #find free sequence number first
        existingex_p = sqp.SQQuery(self._fact, Experiment).where((Experiment.ProjectId==self._proj._id) & (Experiment.Sequence >= 0)).order_by(Experiment.Sequence).select(lambda ex : ex.sequence)
        exexs = list(existingex_p)
        #we have a ordered list of existing sequence numbers here

        if len(exexs) > 0:
            newseq = exexs[-1]+1
        else:
            newseq = 1

        desc = "Exp #{}".format(newseq)
        exp = Experiment(sequence=newseq, 
            description=desc,
            projectid=self._proj._id,
            printerused=self._printer,
            printerusedid=self._printer._id,
            extruderused=self._extruder,
            extruderusedid=self._extruder._id)

        self._fact.flush(exp)
        exp.factors = []
        
        #create uninitialised values
        for fprep in self._factpreps:
            factv = FactorValue(experimentid=exp._id,
                factordefinition=fprep.factordefinition,
                factordefinitionid=fprep.factordefinition._id)
            self._fact.flush(factv)
            exp.factors.append(factv)

        self.write_resps(exp)
        self.write_enviros(exp)

        return (1, exp)
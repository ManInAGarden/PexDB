from enum import Enum
import sqlitepersist as sqp
from PersistClasses import *

class CreaSequenceEnum(Enum):
    LINEAR = 0 #experiments are created in the same sequence as defined
    MIXED = 1 #exps are created in a random sequence


        
class _CreaBase:
    """basic class for experiment creation, do not use directly, only use derivated classes"""

    def __init__(self, fact : sqp.SQFactory, 
            project : Project, 
            printer: Printer, 
            extruder : Extruder):

        self._fact = fact
        self._proj = project
        self._printer = printer
        self._extruder = extruder
        self._preparethepreps()


    def _preparethepreps(self):
        """prepare to have the definitions of factors and responses for the given project ready to be used"""
        factpreps_q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._proj._id)
        self._factpreps = list(factpreps_q) #we store the preps which we will need more than once
        resppreps_q = sqp.SQQuery(self._fact, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._proj._id)
        self._resppreps = list(resppreps_q)
        envpreps_q = sqp.SQQuery(self._fact, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==self._proj._id)
        self._envpreps = list(envpreps_q)

    def write_resps(self, exp : Experiment):
        """ Writes the responses (one for each prepared response) for the current experiment.
            All values are initialised with 0
        """
        if exp.responses is None:
            exp.responses = []
            
        for respprep in self._resppreps:
            resdef = respprep.responsedefinition
            resp = ResponseValue(experimentid=exp._id, 
                responsedefinition=resdef,
                responsedefinitionid=resdef._id,
                value = 0.0)

            self._fact.flush(resp)
            exp.responses.append(resp)

    def write_enviros(self, exp : Experiment):
        if exp.enviros is None:
            exp.enviros = []
            
        for envprep in self._envpreps:
            envval = EnviroValue(experimentid = exp._id,
                    envirodefinitionid = envprep.envirodefinitionid,
                    envirodefinition=envprep.envirodefinition,
                    value = 0.0)
            self._fact.flush(envval)
            exp.enviros.append(envval)

    def _get_level_arr(self):
        """ creates and returns a list of the levels in each factor in the sequence defined in
            self._factpreps
        """
        answ = []

        for fprep in self._factpreps:
            answ.append(fprep.levelnum)

        return answ

    def create(self):
        raise Exception("override create in your own class, do not use method in _CreaBase!!!!")


class _CreaSequential(_CreaBase):

    def __init__(self, fact : sqp.SQFactory, 
            project : Project, 
            printer: Printer, 
            extruder : Extruder,
            sequence : CreaSequenceEnum = CreaSequenceEnum.LINEAR,
            planneddt: datetime = None,
            repetitions : int=1,
            docentre : bool=False):

        super().__init__(fact, project, printer, extruder)
        self._sequence = sequence
        self._planneddt = planneddt
        self._repetitions = repetitions
        self._docentre = docentre

    def _getcentre(self):
        """ get the factors for a centre experiment
            i.e. a list of all factors at their centred (middle of [min,max]) values
        """
        answ = []
        for p in self._factpreps:
            min = p.minvalue
            max = p.maxvalue
            lvls = p.levelnum

            currval = min + (max - min)/2.0

            answ.append(FactorValue(factordefinition=p.factordefinition,
                factordefinitionid=p.factordefinitionid,
                value = currval))

        return answ

    def write_linear(self, result):
        expct = 0

        for i in range(self._repetitions):
            for res in result:
                exp = Experiment(sequence=expct + 1,
                    repnum = i+1,
                    description="Exp #{}".format(expct+1),
                    project = self._proj,
                    projectid = self._proj._id,
                    printerused = self._printer,
                    printerusedid = self._printer._id,
                    extruderused = self._extruder,
                    extruderusedid = self._extruder._id,
                    carriedoutdt=self._planneddt)
                self._fact.flush(exp) #we need the _id

                for factval in res:
                    factval.experimentid = exp._id
                    self._fact.flushcopy(factval)

                self.write_resps(exp) #write the prepared responses
                self.write_enviros(exp)
                expct += 1

        return expct

    def write_mixed(self, result):
        expct = 0
        rnum = 0
        for res in RandHelper(result, self._repetitions):
            exp = Experiment(sequence=expct + 1,
                repnum = rnum + 1,
                description="Exp #{}".format(expct+1),
                project = self._proj,
                projectid = self._proj._id,
                printerused = self._printer,
                printerusedid = self._printer._id,
                extruderused = self._extruder,
                extruderusedid = self._extruder._id)
            self._fact.flush(exp) #we need the _id

            for factval in res:
                factval.experimentid = exp._id
                self._fact.flushcopy(factval)

            self.write_resps(exp) #write the prepared responses
            self.write_enviros(exp)

            expct += 1
            if expct % len(result) == 0:
                rnum = 0
            else:
                rnum += 1

        return expct
    

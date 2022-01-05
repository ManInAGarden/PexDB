from enum import Enum
import sqlitepersist as sqp
from PersistClasses import *

class CreaSequenceEnum(Enum):
    LINEAR = 0 #experiments are created in the same sequence as defined
    MIXED = 1 #exps are created in a random sequence


class LevelOverflow(Exception):
    pass

class LevelCounter():
    def __init__(self, preps):
        self._stagemax = []
        self._currlevels = []

        for prep in preps:
            self._stagemax.append(prep.levelnum)
            self._currlevels.append(0)

    @property
    def currlevels(self):
        return list(self._currlevels)

    def increment(self):
        """add one to the counter"""
        done = False
        for i in range(len(self._currlevels)):
            self._currlevels[i] += 1
            if self._currlevels[i] < self._stagemax[i]:
                done = True
                break
            else:
                self._currlevels[i] = 0 #overflow
                
        if not done:
            raise LevelOverflow("Level overflow in LevelCounter")

        return list(self._currlevels)
        
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

    def create(self):
        raise Exception("override create in your own class, do not use method in _CreaBase!!!!")



class _CreaSequential(_CreaBase):

    def __init__(self, fact : sqp.SQFactory, 
            project : Project, 
            printer: Printer, 
            extruder : Extruder,
            sequence : CreaSequenceEnum = CreaSequenceEnum.LINEAR,
            planneddt: datetime = None,
            repetitions : int=1):

        super().__init__(fact, project, printer, extruder)
        self._sequence = sequence
        self._planneddt = planneddt
        self._repetitions = repetitions

    

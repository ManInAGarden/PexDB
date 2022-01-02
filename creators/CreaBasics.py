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
            sequence : CreaSequenceEnum = CreaSequenceEnum.LINEAR):

        super().__init__(fact, project, printer, extruder)
        self._sequence = sequence

    

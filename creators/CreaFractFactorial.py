import sqlitepersist as sqp
from PersistClasses import *
from .CreaBasics import *
from .CreaBasics import _CreaSequential, _CreaBase
from pyDOE2 import *

class CreaFractFactorial(_CreaSequential):
    """ class for creation of fractional factorial experiment schemes
    """
    
    def __init__(self, 
        fact: sqp.SQFactory, 
        project: Project, 
        printer: Printer, 
        extruder: Extruder, 
        sequence: CreaSequenceEnum = CreaSequenceEnum.LINEAR,
        planneddt: datetime = None,
        repetitions : int=1,
        combidef : str = None):
        
        super().__init__(fact, project, printer, extruder, sequence=sequence, planneddt=planneddt, repetitions=repetitions)

        if combidef is None or len(combidef)==0:
            raise Exception("A fractional factorial with no combination directives makes no sense!")

        self._combidef = self._trans_cd(combidef)
        

    def _trans_cd(self, cdefs):
        pass
    
    def _preparethepreps(self):
        super()._preparethepreps()

        self._redfactpreps = []
        for fprep in self._factpreps:
            if fprep.factordefinition.name not in self._ommitfactors:
                self._redfactpreps.append(fprep)


    def create(self):
        """ create all experiments in a "fractional factorial 2 level each" schema
        """
        result = []

       
        allidxes = fracfact(self._combidef) #_combidef is already translated from fact_abbreviations to A,B,C... form
        for idxes in allidxes:
            factline = self._getfactors(idxes)
            # self._dbgprint(idxes, factline)
            result.append(factline)

        if self._sequence is CreaSequenceEnum.MIXED:
            expct = self.write_mixed(result)
        elif self._sequence is CreaSequenceEnum.LINEAR:
            expct = self.write_linear(result)
        else:
            raise Exception("unknown sequence value {}".format(str(self._sequence)))

        return expct
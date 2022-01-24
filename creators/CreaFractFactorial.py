import sqlitepersist as sqp
from PersistClasses import *
from .CreaBasics import *
from .CreaBasics import _CreaSequential, _CreaBase

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
        ommitfactors : list = None):
        
        super().__init__(fact, project, printer, extruder, sequence=sequence, planneddt=planneddt, repetitions=repetitions)

        if ommitfactors is None:
            raise Exception("Partly factorial with no ommits makes no sense!")

        self._ommitfactors = ommitfactors
        

    def _preparethepreps(self):
        super()._preparethepreps()

        self._redfactpreps = []
        for fprep in self._factpreps:
            if fprep.factordefinition.name not in self._ommitfactors:
                self._redfactpreps.append(fprep)


    def create(self):
        """ create all factors in combinations not in ommit-factors of values 
            according to all their defined levels
        """
        result = []
        idxhistory = []

        lvlct = LevelCounter(self._redfactpreps)
        try:
            idxes = lvlct.currlevels
            while True: #do this until we get the level overflow esception
                idxhistory.append(idxes)
                factline = self._getfactors(idxes)
                # self._dbgprint(idxes, factline)
                result.append(factline)
                idxes = lvlct.increment()
        except LevelOverflow:
            pass

        if self._sequence is CreaSequenceEnum.MIXED:
            expct = self.write_mixed(result)
        elif self._sequence is CreaSequenceEnum.LINEAR:
            expct = self.write_linear(result)
        else:
            raise Exception("unknown sequence value {}".format(str(self._sequence)))

        return expct
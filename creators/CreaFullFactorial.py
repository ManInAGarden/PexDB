from datetime import date, datetime
from enum import Enum
import random
import sqlitepersist as sqp
from PersistClasses import *

from .CreaBasics import _CreaBase, _CreaSequential, CreaSequenceEnum

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


class CreaFullFactorial(_CreaSequential):
    """creates one experiment for every combination of factor levels defined in the given 
    project's factor preparations"""

    def __init__(self, fact: sqp.SQFactory, project: Project, printer: Printer, extruder: Extruder, sequence: CreaSequenceEnum = ...):
        super().__init__(fact, project, printer, extruder, sequence=sequence)

    def _getfactors(self, idxes : list):
        answ = []
        for i in range(len(idxes)):
            p = self._factpreps[i]
            min = p.minvalue
            max = p.maxvalue
            lvls = p.levelnum

            currval = min + idxes[i]*(max - min)/(lvls-1)

            answ.append(FactorValue(factordefinition=p.factordefinition,
                factordefinitionid=p.factordefinitionid,
                value = currval))

        return answ

    def _dbgprint(self, idxes, factline):
        for idx in idxes:
            print("{}, ".format(idx))

        for fact in factline:
            print("{}, ".format(fact.value))


    def create(self):
        """create all factors in combinations of values according to all their defined levels"""
        result = []
        idxhistory = []

        lvlct = LevelCounter(self._factpreps)
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

    def write_linear(self, result):
        expct = 0

        for res in result:
            exp = Experiment(sequence=expct + 1, 
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
                self._fact.flush(factval)

            self.write_resps(exp) #write the prepared responses
        
            expct += 1
            
        return expct

    def write_mixed(self, result):
        expct = 0
        while len(result) > 0:
            residx = random.randint(0, len(result)-1) #randomize the sequence!
            res = result[residx]

            exp = Experiment(sequence=expct + 1, 
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
                self._fact.flush(factval)

            self.write_resps(exp) #write the prepared responses

            result.pop(residx)
            expct += 1
        
        return expct

    

        
        
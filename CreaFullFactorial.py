from datetime import date, datetime
from enum import Enum
import random
import sqlitepersist as sqp
from itertools import combinations, permutations
from PersistClasses import *


class LevelOverflow(Exception):
    pass

""" class LevelCounter(object):
    def __init__(self, preps):
        self._currpos = 0
        self._lvlmax = []
        self._currlevels = []
        self._overflow = False
        for prep in preps:
            self._lvlmax.append(prep.levelnum-1)
            self._currlevels.append(0)

    @property
    def stage(self):
        return self._currpos

    def reset(self):
        self._currpos = 0
        self._overflow = False
        for i in range(len(self._currlevels)):
            self._currlevels[i] = 0

    def get_maxcountforstage(self, stage):
        if stage > len(self._lvlmax):
            raise Exception("Stage # {} does not exist in levelcounter. Maximum stage is {}".format(stage, len(self._lvlmax)))

        return self._lvlmax[stage]

    def get_current(self):
        return list(self._currlevels) #return a clone of the list without incrementing anything


    def get_next(self):
        if self._overflow:
            raise Exception("Already in overlfow, do not call get_next anymore")

        if self._currlevels[self._currpos] < self._lvlmax[self._currpos]:
            self._currlevels[self._currpos] += 1
        else:
            self._currpos += 1
            if self._currpos >= len(self._lvlmax):
                self._overflow = True
                raise LevelOverflow("Level overflow - no more levels")
            
            self._currlevels[self._currpos] += 1

        return list(self._currlevels) #return a clone of the list

    def next_stage(self):
        if self._overflow:
            raise Exception("Already in overlfow, do not call get_next anymore")

        self._currpos += 1

        if self._currpos >= len(self._lvlmax):
            raise LevelOverflow("Level overflow - no more levels")

        return self

    def has_smaller_stage(self, other):
        return self._currpos < other._currpos


    def __eq__(self, other):
        if not type(other) is LevelCounter:
            raise Exception("equality not declared for other object, which is of type {0}".format(str(type(other))))

        if len(self._currlevels) != len(other._currlevels):
            raise Exception("Only level counters of the same dimension can be compared!")

        if self._currpos != other._currpos:
            return False

        for i in range(len(self._currlevels)):
            if self._currlevels[i] != other._currlevels[i]:
                return False

        return True

    def __lt__(self, other):
        if not type(other) is LevelCounter:
            raise Exception("Comparision "<" is not declared for other object, which is of type {0}".format(str(type(other))))
        
        if len(self._currlevels) != len(other._currlevels):
            raise Exception("Only level counters of the same dimension can be compared!")

        if self._currpos < other._currpos:
            return True
        elif self._currpos > other._currpos:
            return False

        return self._currlevels[self._currpos] < other._currlevels[other._currpos] """


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



class CreaSequenceEnum(Enum):
    LINEAR = 0 #experiments are created in the same sequence as defined
    MIXED = 1 #exps are created in a random sequence

class CreaFullFactorial:
    """creates one experiment for every combination of factor levels defined in the given 
    project's factor preparations"""

    def __init__(self, fact : sqp.SQFactory, 
            project : Project, 
            printer: Printer, 
            extruder : Extruder,
            sequence : CreaSequenceEnum = CreaSequenceEnum.LINEAR):

        self._fact = fact
        self._proj = project
        self._printer = printer
        self._extruder = extruder
        self._sequence = sequence

    def _prepare(self):
        preps_q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._proj._id)
        self._preps = list(preps_q) #we store the preps which we will need more than once
        
    def _getfactors(self, idxes : list):
        answ = []
        for i in range(len(idxes)):
            p = self._preps[i]
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
        self._prepare()
        result = []
        idxhistory = []

        lvlct = LevelCounter(self._preps)
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

    def create_old(self):
        """create all factors in combinations of values according to all their defined levels"""
        self._prepare()
        self._factors = []

        result = []
        idxhistory = []
        movingcounter = LevelCounter(self._preps)
        maxlevel = len(self._preps)
        lvl = 1
        while lvl < maxlevel:
            if lvl == 1:
                topcount = 0
            else:
                topcount = 1
                
            maxtopcount = movingcounter.get_maxcountforstage(lvl)
            while topcount <= maxtopcount:
                movingcounter.reset()
                idxes = movingcounter.get_current()
                while movingcounter.stage < lvl:
                    idxes[lvl] = topcount #we set the counters toplevel result to make this count upwards too
                    idxhistory.append(idxes) #nice for debugging of the algorithm
                    factline = self._getfactors(idxes)
                    # self._dbgprint(idxes, factline)
                    result.append(factline)
                    idxes = movingcounter.get_next()


                topcount += 1

            lvl += 1

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
            exp = Experiment(carriedoutdt=datetime.now(), 
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

            expct += 1
            
        return expct

    def write_mixed(self, result):
        expct = 0
        while len(result) > 0:
            residx = random.randint(0, len(result)-1) #randomize the sequence!
            res = result[residx]

            exp = Experiment(carriedoutdt=datetime.now(), 
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

            result.pop(residx)
            expct += 1
        
        return expct

        
        
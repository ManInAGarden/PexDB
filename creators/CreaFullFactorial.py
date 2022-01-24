from datetime import date, datetime
from enum import Enum
import random
import sqlitepersist as sqp
from PersistClasses import *

from .CreaBasics import CreaSequenceEnum, _CreaSequential
from pyDOE2 import *


class RandHelper:
    def __init__(self, results : list, num_of_reps : int):
        self._results = results
        self._num_of_reps = num_of_reps


    def __iter__(self):
        self._ranmem = []
        i = 0
        for res in self._results:
            self._ranmem.append([])
            for j in range(self._num_of_reps):
                self._ranmem[i].append(res)

            i += 1

        return self

    def __next__(self):
        ll = len(self._ranmem)

        if ll == 0:
            raise StopIteration

        if ll == 1:
            l = 0
        else:
            l = random.randint(0, ll - 1)

        lc = len(self._ranmem[l])
        if lc <= 1:
            c = 0
        else:
            c = random.randint(0, lc - 1)

        print("getting l={}, c={}".format(l, c))
        answ = self._ranmem[l][c]

        self._ranmem[l].pop(c)
        if len(self._ranmem[l])==0:
            self._ranmem.pop(l)

        return answ

class CreaFullFactorial(_CreaSequential):
    """creates one experiment for every combination of factor levels defined in the given
    project's factor preparations"""

    def __init__(self,
        fact: sqp.SQFactory,
        project: Project,
        printer: Printer,
        extruder: Extruder,
        sequence: CreaSequenceEnum = CreaSequenceEnum.LINEAR,
        planneddt: datetime = None,
        repetitions : int=1,
        docentre : bool=False):

        super().__init__(fact,
            project, printer, extruder,
            sequence=sequence,
            planneddt=planneddt,
            repetitions=repetitions,
            docentre = docentre)

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

        allidxes = fullfact(self._get_level_arr())
        for idxes in allidxes:
            factline = self._getfactors(idxes)
            # self._dbgprint(idxes, factline)
            result.append(factline)

        if self._docentre:
            factline = self._getcentre()
            result.append(factline)

        if self._sequence is CreaSequenceEnum.MIXED:
            expct = self.write_mixed(result)
        elif self._sequence is CreaSequenceEnum.LINEAR:
            expct = self.write_linear(result)
        else:
            raise Exception("unknown sequence value {}".format(str(self._sequence)))

        return expct

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





from datetime import date, datetime
from enum import Enum
import random
import sqlitepersist as sqp
from PersistClasses import *

from .CreaBasics import CreaSequenceEnum, _CreaSequential
from pyDOE2 import *




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

    





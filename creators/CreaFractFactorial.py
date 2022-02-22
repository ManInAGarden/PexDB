from pydoc import doc
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
        docentre : bool=False):

        #prepare the preps is called somewhere down here...
        super().__init__(fact, project, printer, extruder, sequence=sequence, planneddt=planneddt, repetitions=repetitions, docentre=docentre)


    def _getletter(self, num : int):
        assert num >= 0 and num <= 26

        return chr(num + 65)

    def _preparethepreps(self):
        super()._preparethepreps()

        #create a translation dicts for fact abbreviations
        #and vor fact single letter names -> abbreviations
        self._abbrletterdict = {}
        self._abbrfactdict = {}
        #add all factors we can find to helper dict, just to make sure we
        letterct = 0
        for fprep in self._factpreps:
            self._fact.fill_joins(fprep, 
                ProjectFactorPreparation.FactorCombiDefs)
            fdef = fprep.factordefinition
            
            if fdef.abbreviation not in self._abbrfactdict:
                self._abbrfactdict[fdef.abbreviation] = fdef
                self._abbrletterdict[fdef.abbreviation] = self._getletter(letterct)
                letterct += 1

            if fprep.iscombined:
                for inter in fprep.factorcombidefs:
                    fdef = inter.factordefinition
                    if fdef.abbreviation not in self._abbrfactdict:
                        self._abbrfactdict[fdef.abbreviation] = fdef
                        self._abbrletterdict[fdef.abbreviation] = self._getletter(letterct)
                        letterct += 1

        self._combstr = self._get_combstr()

    def _get_combstr(self):
        """ from the combinations in self._combidefs and the prepared translations a string
            describing the combinations with only capital letters is produced and returned
        """
        if self._factpreps is None or len(self._factpreps) <= 0:
            raise Exception("No factor prepearations found while trying to create the combinations string!")

        first = True
        for fprep in self._factpreps:
            if first:
                answ = ""
                first = False
            else:
                answ += " "

            if fprep.isnegated:
                answ += "-"

            if not fprep.iscombined:
                answ += self._abbrletterdict[fprep.factordefinition.abbreviation]
            else:
                self._fact.fill_joins(fprep, ProjectFactorPreparation.FactorCombiDefs)
                for inter in fprep.factorcombidefs:
                    answ += self._abbrletterdict[inter.factordefinition.abbreviation]

        return answ

    def _getfactors(self, idxes : list):
        answ = []
        for i in range(len(idxes)):
            p = self._factpreps[i]
            min = p.minvalue
            max = p.maxvalue
            lvls = p.levelnum

            if lvls != 2:
                raise Exception("Fractional factored experiments do only allow two levels! Please correct your factor preparations")

            if idxes[i] == 1:
                currval = max
            elif idxes[i] == -1:
                currval = min
            else:
                raise Exception("Index must be -1 or 1. Value of {} encountered as index for factor calculation".format(idxes[i]))

            answ.append(FactorValue(factordefinition=p.factordefinition,
                factordefinitionid=p.factordefinitionid,
                value = currval))

        return answ

    def create(self):
        """ create all experiments in a "fractional factorial 2 level each" schema
        """
        result = []
        allidxes = fracfact(self._combstr) #_combstr is already translated from fact_abbreviations to A,B,C... form
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
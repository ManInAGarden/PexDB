from datetime import datetime
import sqlitepersist as sqp
from PersistClasses import *

class CreaFullFactorial:
    """creates one experiment for every combination of factor levels defined in the given 
    project's factor preparations"""

    def __init__(self, fact : sqp.SQFactory, project : Project):
        self._fact = fact
        self._proj = project

    def create(self):
        preps_q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._proj._id)
        preps = list(preps_q)
        expct = 0
        valdict = {} #dictionary of values used in experiment preparation

        #prepare the valdict
        for p in preps:
            valdict[p.factordefinitionid] = None
        
        expct = 1
        for row_prep in preps:
            for rl in range(row_prep.levelnum):
                row_val = row_prep.minvalue + rl*(row_prep.maxvalue - row_prep.minvalue)/row_prep.levelnum
                valdict[row_prep.factordefinitionid] = row_val
                for col_prep in preps:
                    for cl in range(col_prep.levelnum):
                        col_val = col_prep.minvalue + rl*(col_prep.maxvalue - col_prep.minvalue)/col_prep.levelnum
                        valdict[col_prep.factordefinitionid] = col_val

                        cexp = Experiment(projectid=self._proj._id, name="Exp # {0}".format(expct),
                                        carriedoutdt=datetime.now())
                        expct += 1
                        self._fact.flush(cexp) # we need the _id

                        for key, value in valdict.items():
                            factval = FactorValue(factordefinitionid=key, value=value, experimentid = cexp._id)
                            self._fact.flush(factval)



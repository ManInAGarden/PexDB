import pandas as pas
import sqlitepersist as sqp
from PersistClasses import *

class MultiReg():
    """class to solve a multi linear regression problem based on data from a project"""
    def __init__(self, fact : sqp.SQFactory	, project : Project):
        self._f = fact
        self._p = project
        self._pid = project._id
        self._df = None
        self._experiments = None
        self._factdict = {}
        self._respdict = {}

    @property
    def factdict(self):
        return self._factdict

    @property
    def respdict(self):
        return self._respdict

    @property
    def dataframe(self):
        if self._df is None:
            raise Exception("Dataframe has not been built yet")
        return self._df

    def _get_experiments(self):
        expi_q = sqp.SQQuery(self._f, Experiment).where(Experiment.ProjectId==self._pid).order_by(Experiment.Repnum)
        return list(expi_q)
    
    def _get_emptydf(self):
        answ = {}

        answ["repnum"] = []
        fpreps_q = sqp.SQQuery(self._f, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._pid)
        for fprep in fpreps_q:
            bname = fprep.factordefinition.abbreviation
            self._factdict[bname] = fprep.factordefinition
            answ[bname] = []

        rpreps_q = sqp.SQQuery(self._f, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._pid)

        for respdef in rpreps_q:
            bname = respdef.responsedefinition.abbreviation
            self._respdict[bname] = respdef.responsedefintion
            answ[bname] = []

        return answ

    def _get_dataframe(self):
        """creates the dataframe used for linerar regression
            -> new dataframe with columns for all factors, responses, and
                standard deviation and variance for all responses. The
                latter are only non zero when repetitions are in the experiments
        """
        data = self._get_emptydf() #create the empty dataframe

        for exp in self._experiments:
            self._f.fill_joins(exp, Experiment.Factors, Experiment.Responses)
            data["repnum"].append(exp.repnum)

            for fact in exp.factors:
                data[fact.factordefinition.abbreviation].append(fact.value)

            for resp in exp.responses:
                rnam = resp.responsedefinition.abbreviation
                data[rnam].append(resp.value)
                data[rnam+"#vari"].append(0.0)
                data[rnam+"#stddev"].append(0.0)

        return data


    def read_data(self):
        """read the data for indipendent and dependent variables to an internal dataframe"""
        self._experiments = self._get_experiments()
        ddict = self._get_dataframe()
        self._df = pas.DataFrame(ddict)
        return self._df


    def solve_for(self, indiname : str):
        pass
        
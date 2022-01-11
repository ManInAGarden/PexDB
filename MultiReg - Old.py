import pandas as pas
from pandas.core.series import Series
import statsmodels.api as sma
import sqlitepersist as sqp
from PersistClasses import *

class MultiReg():
    """class to solve a multi linear regression problem based on data from a project"""
    def __init__(self, fact : sqp.SQFactory	, project : Project):
        self._f = fact
        self._p = project
        self._pid = project._id
        self._df = None #ras data frame
        self._grpdf = None #grouped dataframe
        self._grpdff = None #flattened grouped data frame
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
        return self._grpdff #return the grouped dataframe

    @property
    def meanframe(self):
        return self._grpdf

    @property
    def rawframe(self):
        if self._df is None:
            raise Exception("Dataframe has not been built yet")

        return self._df
        

    def _get_experiments(self):
        expi_q = sqp.SQQuery(self._f, Experiment).where(Experiment.ProjectId==self._pid).order_by(Experiment.Repnum)
        return list(expi_q)
    
    def _get_emptydf(self):
        answ = {}

        answ["repnum"] = []
        answ["#factkey"] = []
        fpreps_q = sqp.SQQuery(self._f, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._pid)
        for fprep in fpreps_q:
            bname = fprep.factordefinition.abbreviation
            self._factdict[bname] = fprep.factordefinition
            answ[bname] = []

        rpreps_q = sqp.SQQuery(self._f, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._pid)

        for respdef in rpreps_q:
            bname = respdef.responsedefinition.abbreviation
            self._respdict[bname] = respdef.responsedefinition
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
            if exp.repnum is not None:
                data["repnum"].append(exp.repnum)
            else:
                data["repnum"].append(0)

            factkey = None
            first = True
            for fact in exp.factors:
                data[fact.factordefinition.abbreviation].append(fact.value)
                if first:
                    factkey = str(fact.value)
                    first = False
                else:
                    factkey += "#" + str(fact.value)

            data["#factkey"].append(factkey)

            for resp in exp.responses:
                rnam = resp.responsedefinition.abbreviation
                data[rnam].append(resp.value)

        return data


    def read_data(self):
        """read the data for indipendent and dependent variables to an internal dataframe"""
        self._experiments = self._get_experiments()
        ddict = self._get_dataframe()
        self._df = pas.DataFrame(ddict)
        self._grpdf = self._df.groupby(["#factkey"])
        meanl = list(self._factdict.keys()).extend(self._respdict.keys())
        self._grpdff = self._grpdf.mean(meanl)
        self._grpdff = self._grpdff.reset_index()

    def solve_for(self, dependiname : str):
        """solve the lin regression for a given dependent variable"""
        y = self.dataframe[dependiname]
        x_names = list(self._factdict.keys())
        X = self.dataframe[x_names]
        X = sma.add_constant(X)
        self.model = sma.OLS(y, X).fit()
        predictions = self.model.predict(X)
        summary = self.model.summary()

        return predictions, summary

    def get_formula(self, floatforms : str):
        answ = "<{}> = ".format(self.respdict[self.model.model.endog_names].name)
        answ += floatforms.format(self.model.params["const"])
        for abbr, fact in self.factdict.items():
            flt = self.model.params[abbr]
            if abs(flt) < 1e-6:
                continue

            if flt > 0.0:
                answ += " + "
            elif flt < 0.0:
                answ += " - "
                flt *= -1

            answ += floatforms.format(flt) + "*" + "<{}>".format(fact.name)

        return answ

    def predict(self, x : list):
        """predict a response for a single combination or many combinations of factors
        x is list -> single response value
        x is array -> multiple predictions"""
        if self.model is None:
            raise Exception("Please solve befor predicting")

        return self.model.predict(x.append(1.0))


        
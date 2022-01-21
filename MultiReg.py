import pandas as pas
from pandas.core.series import Series
#import statsmodels.api as sma
from sklearn.linear_model import LinearRegression
from Evaluator import Evaluator
import sqlitepersist as sqp
from PersistClasses import *

class MultiReg():
    MERGENAME = "#MERGEDRESPS#"

    """class to solve a multi linear regression problem based on data from a project"""
    def __init__(self, fact : sqp.SQFactory	, project : Project, normed = False):
        self._f = fact
        self._p = project
        self._normed = normed
        self._pid = project._id
        self._df = None #ras data frame
        self._grpdf = None #grouped dataframe
        self._grpdff = None #flattened grouped data frame
        self._experiments = None
        self._factdict = {}
        self._respdict = {}
        self._fprep_minmax = {}
        self._mergeformula = None # None means we do no response merging

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

    @property
    def resp_abbreviations(self):
        return list(self._respdict.keys())

    @property
    def fact_abbreviations(self):
        return list(self._factdict.keys())
        

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
            self._fprep_minmax[bname] = (fprep.minvalue, fprep.maxvalue)
            answ[bname] = []

        rpreps_q = sqp.SQQuery(self._f, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._pid)

        for respdef in rpreps_q:
            bname = respdef.responsedefinition.abbreviation
            self._respdict[bname] = respdef.responsedefinition
            answ[bname] = []

        if self._p.domergecalculation is True and self._p.mergeformula is not None and len(self._p.mergeformula)>0:
            self._mergeformula = self._p.mergeformula
            bname = MultiReg.MERGENAME
            self._respdict[bname] = ResponseDefinition(name="merged_response", abbreviation=bname) #we never flush this!
            answ[bname] = []

        return answ

    def get_factval(self, factor : FactorValue):
        """ get the value itself or the normalized value, depending on the state of self._normed"""
        bname = factor.factordefinition.abbreviation
        return self.get_factval_r(bname, factor.value)

    def get_factval_r(self, bname : str, val : float):
        """ get a value normalized/standardized in case normalized is set
            for the solver. Otherwise get the val itself
            bname : abbreviation/name of the factor
            val : the value to eventually be normalized
        """
        if not self._normed:
            return val

        min = self._fprep_minmax[bname][0]
        max = self._fprep_minmax[bname][1]
        l = (max-min)/2
        val = (val - min)/l - 1.0
        return val
    

        
    def _get_dataframe(self):
        """creates the dataframe used for linerar regression
            -> new dataframe with columns for all factors, responses, and
                standard deviation and variance for all responses. The
                latter are only non zero when repetitions are in the experiments
        """
        data = self._get_emptydf() #create the empty dataframe
        ev = Evaluator()

        for exp in self._experiments:
            self._f.fill_joins(exp, Experiment.Factors, Experiment.Responses)
            if exp.repnum is not None:
                data["repnum"].append(exp.repnum)
            else:
                data["repnum"].append(0)

            factkey = None
            first = True
            for fact in exp.factors:
                fval = self.get_factval(fact)
                data[fact.factordefinition.abbreviation].append(fval)
                if first:
                    factkey = str(fval)
                    first = False
                else:
                    factkey += "#" + str(fval)

            data["#factkey"].append(factkey)
            merge_respvalues = {}
            for resp in exp.responses:
                rnam = resp.responsedefinition.abbreviation
                data[rnam].append(resp.value)
                merge_respvalues[self._replace_spaces(resp.responsedefinition.name)] = resp.value

            if self._mergeformula is not None:
                self._fillmissing(merge_respvalues, 0.0)
                data[MultiReg.MERGENAME].append(ev.eval_formula(self._mergeformula,
                    merge_respvalues))

        return data

    def _fillmissing(self, valdict, default):
        for fabbr, respdef in self._respdict.items():
            kexn = self._replace_spaces(respdef.name)
            if fabbr != MultiReg.MERGENAME and kexn not in valdict.keys():
                valdict[kexn] = default

    def _replace_spaces(self, ins : str) -> str:
        if ins is None:
            return None

        return ins.replace(" ", "_")

    def read_data(self):
        """read the data for indipendent and dependent variables to an internal dataframe"""
        self._experiments = self._get_experiments()
        ddict = self._get_dataframe()
        self._df = pas.DataFrame(ddict)
        self._grpdf = self._df.groupby(["#factkey"])
        meanl = list(self._factdict.keys()).extend(self._respdict.keys())
        self._grpdff = self._grpdf.mean(meanl)
        self._grpdff = self._grpdff.reset_index()

    def solve_for_all(self):
        """solve the linear regression for all dependent variables"""
        y_names = self.resp_abbreviations
        y = self.dataframe[y_names]
        x_names = self.fact_abbreviations
        X = self.dataframe[x_names]
        mlr = LinearRegression()
        self.model = mlr.fit(X, y)
        return self.model.coef_, self.model.intercept_

    def solve_for(self, dependiname : str):
        """solve the lin regression for a given dependent variable"""
        y = self.dataframe[dependiname]
        x_names = list(self._factdict.keys())
        X = self.dataframe[x_names]
        mlr = LinearRegression()
        self.model = mlr.fit(X, y)
        return self.model.coef_, self.model.intercept_

    def get_formula(self, floatforms : str, targresp : str):
        """get the formula for a single target"""
        answ = "<{}> = ".format(self.respdict[targresp].name)

        #self.model.coef_, self.model.intercept_
        l = self.resp_abbreviations.index(targresp)
        answ += floatforms.format(self.model.intercept_[l])
        coefs = self.model.coef_[l]
        for abbr, fact in self.factdict.items():
            c = self.fact_abbreviations.index(abbr)
            flt = coefs[c]
            if abs(flt) < 1e-6:
                continue

            if flt > 0.0:
                answ += " + "
            elif flt < 0.0:
                answ += " - "
                flt *= -1

            answ += floatforms.format(flt) + "*" + "<{}>".format(fact.name)

        return answ

    def predict(self, repabbr : str, facts : dict, donormal=True) -> float:
        """ predict a response for a single combination of factors
            repname : name of the response to be predicted
            facts : dictionary containing the names and values of all responses
            donormal : when true normalization will be done when the model is normalized,
            if false values will be used as given in facts
        """
        if self.model is None:
            raise Exception("Please solve befor predicting")

        l = self.resp_abbreviations.index(repabbr)
        cofs = self.model.coef_[l] #get the coefficients for prediction of response repabbr
        y = self.model.intercept_[l] #start with the constant part
        c = 0
        for fabbr in self.fact_abbreviations:
            if donormal:
                y += cofs[c] * self.get_factval_r(fabbr, facts[fabbr])
            else:
                y += cofs[c] * facts[fabbr]
            c += 1

        return y

    def _get_allfacts(self, df, lnum) -> dict:
        """ get all facts from a dataframe for a given line#
            df : the dataframe
            lnum : the line number
            returns a dict with key=names of factors and values = values of the factors fpr the given line number
        """
        answ = {}
        for fabbr in self.fact_abbreviations:
            answ[fabbr] = df[fabbr][lnum]

        return answ

    def _get_allresponses(self, df, lnum):
        """ get all responses from a dataframe for a given line #
            df : the dataframe
            lnum : the number of the line from which data shall be returned
            returns: a dict filled with the values organized by key=name of response, value=value of response for the given line """
        answ = {}
        for rabbr in self.resp_abbreviations:
            answ[rabbr] = df[rabbr][lnum]

        return answ

    def get_residuals(self, respabbr, dataf = None):
        """ get the residuals on the already set factor data
            for a given response
            respabb : name of the response in the solver data
            dataf : datafram for factor data for which the residuals shall be calculated, if None the already known factors will be used
        """

        if not hasattr(self, "model") or self.model is None:
            raise Exception("Please solve before calculating residuals")

        if dataf is None: #use already knonw fact data
            df = self.dataframe
        else:
            df = dataf

        maxl = len(df)
        respv = []
        yv = []
        rv = []
        r2v = []
        for i in range(maxl):
            facts = self._get_allfacts(df, i)
            resps = self._get_allresponses(df, i)
            y = self.predict(respabbr, facts, False)
            realy = resps[respabbr]
            r = realy - y
            r2 = r**2
            respv.append(realy)
            yv.append(y)
            rv.append(r)
            r2v.append(r2)

        return pas.DataFrame({"realval": respv, "predval":yv, "res": rv, "resqd": r2v})


        
import math
import random as rn
from MultiReg import *
from unittest import TestCase
from TestBase import TestBase
from PersistClasses import *
import creators as cr
from sqlitepersist.SQLitePersistQueryParts import SQQuery


class TestLinearRegression(TestBase):
    def setUp(self) -> None:
        super().setUp()

    def _calc_responses(self, proj : Project, coefs : list, consts : list, randw=0.01):
        exps = list(SQQuery(self.Spf, Experiment).where(Experiment.ProjectId==proj._id))

        for exp in exps:
            self.Spf.fill_joins(exp, Experiment.Responses, Experiment.Factors)

            for i in range(len(exp.responses)):
                respval = consts[i]
                for j in range(len(exp.factors)):
                    respval += coefs[i][j]*exp.factors[j].value + rn.random()*randw

                exp.responses[i].value = respval
                self.Spf.flush(exp.responses[i])

    def test_simple(self):
        fpreps = {
            "PRINOZZTEMP": [190,220,2], #factorabbr : [min, max, levels]
            "MATFLOW" : [80, 110, 2]
        }
        rpreps = {
            "DIMACC" : [1.0], #combination weight - deprecated, not used for anything!
            "SURFQUAL" : [1.0]
        }

        cnum, proj = self.Mck.create_fullfactorial_experiments(fpreps, 
            rpreps, 
            projectname="test_simple_project")

        assert cnum == 4 #two factors with two levels each, 2**2 experiments should have been created here

        M = [
                [-1.0, 0.9],
                [-2.0, -0.5]
            ]
        c = [0.3, 1.5]
        self._calc_responses(proj, M, c)

        lr = MultiReg(self.Spf, proj)
        lr.read_data()

        assert lr.dataframe is not None

        for fpabbr, fpdta in fpreps.items():
            assert len(lr.dataframe[fpabbr]) == 4

        for rpabbr, rpdta in rpreps.items():
            assert len(lr.dataframe[rpabbr]) == 4

        lr.solve_for_all()

        assert lr.model is not None
        coef = lr.model.coef_
        interc = lr.model.intercept_

        allow = 0.5
        for i in range(len(M)):
            for j in range(len(M[i])):
                assert math.fabs(coef[i][j] - M[i][j]) <= allow

        for i in range(len(interc)):
            assert math.fabs(interc[i] - c[i]) <= allow


    def test_standarized(self):
        fpreps = {
            "PRINOZZTEMP": [190,220,2], #factorabbr : [min, max, levels]
            "MATFLOW" : [80, 110, 2]
        }
        rpreps = {
            "DIMACC" : [1.0], #combination weight - deprecated, not used for anything!
            "SURFQUAL" : [1.0]
        }

        cnum, proj = self.Mck.create_fullfactorial_experiments(fpreps, 
            rpreps, 
            projectname="test_simple_project")
            
        assert cnum == 4 #two factors with two levels each, 2**2 experiments should have been created here

        M = [
                [-1.0, 0.9],
                [-2.0, -0.5]
            ]
        c = [0.3, 1.5]
        self._calc_responses(proj, M, c)

        lr = MultiReg(self.Spf, proj, normed=True)
        lr.read_data()

        assert lr.dataframe is not None

        for fpabbr, fpdta in fpreps.items():
            assert len(lr.dataframe[fpabbr]) == 4
            for i in range(len(lr.dataframe[fpabbr])):
                assert math.fabs(lr.dataframe[fpabbr][i]) <= 1.0

        for rpabbr, rpdta in rpreps.items():
            assert len(lr.dataframe[rpabbr]) == 4

        lr.solve_for_all()

        assert lr.model is not None
        coef = lr.model.coef_
        interc = lr.model.intercept_

    def test_simple_fractional(self):
        fpreps = {
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False},
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": False},
            "FANSPEED" : {"minvalue": 0, "maxvalue": 100, "levelnum": 2, "iscombined": True, "isnegated":False, 
                "factorcombidefs" : ["MATFLOW","PRINOZZTEMP"]}
        }
        rpreps = {
            "DIMACC" : [1.0], #combination weight - deprecated, not used for anything!
            "SURFQUAL" : [1.0]
        }


        cnum, proj = self.Mck.create_fractfactorial_experiments(fpreps, 
            rpreps,
            projectname="test_simple_project")


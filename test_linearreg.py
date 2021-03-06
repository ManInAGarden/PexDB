import math
import random as rn
import numpy
from pyDOE2 import *
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
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False},
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": False}
        }
        rpreps = {
            "DIMACC" : {"combinationweight" : 1.0}, #combination weight - deprecated, not used for anything!
            "SURFQUAL" : {"combinationweight" : 1.0}
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
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False},
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": False}
        }
        rpreps = {
            "DIMACC" : {"combinationweight" : 1.0}, #combination weight - deprecated, not used for anything!
            "SURFQUAL" : {"combinationweight" : 1.0}
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

    def _calc_dev(self, m1, m2):
        """ calculate the max difference of the values in two matrices
        """
        maxdev = 0.0
        if len(m1) != len(m2):
            raise Exception("only matrices, vectors of the same size can be compared")

        for i in range(len(m1)):
            v1 = m1[i]
            v2 = m2[i]
            tv = type(v1)
            if tv is float or tv is int or tv is numpy.float64:
                dev = math.fabs(v1-v2)
                if dev > maxdev:
                    maxdev = dev
            else:
                if len(v1) != len(v2):
                    raise Exception("only matrices, vectors of the same size in all dimensions can be compared")

                for j in range(len(v1)):
                    vi1 = v1[j]
                    vi2 = v2[j]
                    dev = math.fabs(vi1-vi2)
                    if dev > maxdev:
                        maxdev = dev

        return maxdev

    def test_simple_fractional(self):
        fpreps = {
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False},
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": False},
            "FANSPEED" : {"minvalue": 0, "maxvalue": 100, "levelnum": 2, "iscombined": True, "isnegated":False, 
                "factorcombidefs" : ["MATFLOW","PRINOZZTEMP"]}
        }
        rpreps = {
            "DIMACC" : {"combinationweight" : 1.0}, #combination weight - deprecated, not used for anything!
            "SURFQUAL" : {"combinationweight" : 1.0}
        }


        cnum, proj = self.Mck.create_fractfactorial_experiments(fpreps, 
            rpreps,
            projectname="test_simple_project")

        assert cnum == 4

        M = [
                [-1.0, 0.9, 0.45],
                [-2.0, -0.5, 1.32]
            ]
        c = [0.3, 1.5]
        self._calc_responses(proj, M, c)

        lr = MultiReg(self.Spf, proj, normed=False)
        lr.read_data()

        assert lr.dataframe is not None

        #check dataframe
        for fpabbr, fpdta in fpreps.items():
            assert len(lr.dataframe[fpabbr]) == 4

        for rpabbr, rpdta in rpreps.items():
            assert len(lr.dataframe[rpabbr]) == 4

        lr.solve_for_all()

        assert lr.model is not None
        coef = lr.model.coef_
        maxcdev = self._calc_dev(coef, M)
        assert maxcdev < 0.03
        interc = lr.model.intercept_
        maxidev = self._calc_dev(interc, c)
        assert maxidev < 0.1

    def test_fractfact_creation(self):
        res = fracfact("A B AB")
        res = fracfact("AB A B")
        pass




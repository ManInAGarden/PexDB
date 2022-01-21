import unittest
from Evaluator import *
import math

class TestEvaluator(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_basic(self):
        formula = "3.0*3.0*3.0"
        evu = Evaluator()
        erg = evu.eval_formula(formula)
        assert type(erg) is float
        assert erg == 27.0


    def test_variables(self):
        formula = "3.0*x + 12*y"
        evu = Evaluator()
        erg = evu.eval_formula(formula, {"x":1.0, "y":2.0})
        assert erg == (3.0*1.0 + 12*2.0)

    def test_math(self):
        formula = "3.0 * math.cos(x) + 12 * math.sqrt(y)"
        evu = Evaluator()
        erg = evu.eval_formula(formula, {"x":1.0, "y":2.0})
        assert erg == (3.0*math.cos(1.0) + 12*math.sqrt(2.0))
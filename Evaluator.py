import math

class Evaluator(object):
    ALLOWED_NAMES = {
           k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
    ALLOWED_NAMES["math"] = math

    def __init__(self):
        pass

    def eval_formula(self, formula, variables={}):
        code = compile(formula, "<string>", "eval")

        allonames = dict(Evaluator.ALLOWED_NAMES)
        allonames.update(variables)
        for name in code.co_names:
            if name not in Evaluator.ALLOWED_NAMES and name not in variables:
                raise NameError(f"Use of {name} not allowed")

        erg = eval(code, {"__builtins__": {}}, allonames)
        return erg
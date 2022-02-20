""" python prog for creating a dependency lib to be used offline
"""
import wx
import pandas
import numpy
import sklearn.linear_model
import importlib.metadata
import json

class DepCreator(object):
    def __init__(self, fname):
        self._fname = fname
        self._modcoll = []

    def writefile(self):
        with open(self._fname, mode="w") as fp:
            js = json.dump(self._modcoll, fp)

    def add(self, modname):
        try:
            md = importlib.metadata.metadata(modname)
        except ModuleNotFoundError:
            md = {"Name": modname, "Version": "./.", "Summary":"not found"}

        mdd = {"Name": md["Name"], "Version":md["Version"], "Summary":md["Summary"]}
        self._modcoll.append(mdd)


if __name__ == '__main__':
    depc = DepCreator("./ressources/dependencies.json")
    names = ["matplotlib", 
        "pandas", 
        "pyDOE2",
        "scikit-learn",
        "wxPython"]
    for name in names:
        depc.add(name)

    depc.writefile()
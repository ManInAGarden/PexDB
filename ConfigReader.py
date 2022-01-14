import json
import getpass as gpa
import os
import re


class ConfigReader():
    """class to instantiate a configreader, which reads a programs confinguration from a json-file"""

    def __init__(self, filepath):
        self._filepath = filepath
        self.readconfig()

    def readconfig(self):
        with open(self._filepath, 'r', encoding="utf8") as f:
            self._data = json.load(f)
        
    def get_value(self, section : str, cname : str):
        """gets a value from the config out of a config named in cname located in a given section"""

        if not section in self._data:
            raise Exception("section named <{0}> not found in configuration".format(section))

        sectdata = self._data[section]

        if not cname in sectdata:
            raise Exception("no configuration entry named <{0}> found in section <{1}>".format(cname, section))

        return sectdata[cname]

    def get_value_interp(self, section : str, cname : str):
        """get a value from the configuation but interpet any %xxxxx% variable contents with their values
           when the orginal value is a string
        """
        val = self.get_value(section, cname)

        if val is None:
            return val

        if type(val) is not str:
            return val

        return self._interpret(val)


    def _interpret(self, val):
        answ = val
        hits = re.findall("%.+%", val)
        for hit in hits:
            hitenv = hit.removeprefix("%").removesuffix("%")
            if hitenv not in os.environ:
                raise Exception("Variable part <{}> not found in environment".format(hitenv))

            hitrepl = os.environ[hitenv]
            answ = answ.replace(hit, hitrepl)

        return answ

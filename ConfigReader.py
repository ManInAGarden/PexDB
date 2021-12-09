import json


class ConfigReader():
    """class to instatntiate a configreader, which reads a programs confinguration from a json-file"""

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
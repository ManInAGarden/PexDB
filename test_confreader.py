import unittest
from ConfigReader import *

class TestConfigReader(unittest.TestCase):

    def setUp(self) -> None:
        self._conf = ConfigReader("./PexDb.conf")

    def test_get_notexists(self):
        exc = False
        try:
            val = self._conf.get_value("murks", "mix")
        except:
            #we expected that
            exc = True

        assert exc is True

    def test_get(self):
        val = self._conf.get_value("database", "filename")
        assert val is not None
        assert type(val) is str

    def test_get_interpreted(self):
        val = self._conf.get_value("database", "tryinits")
        assert val is not None
        assert type(val) is bool

        val1a = self._conf.get_value("preferences", "stdprinter")
        assert val1a is not None
        assert type(val1a) is str

        val1b = self._conf.get_value_interp("preferences", "stdprinter")
        assert val1b is not None
        assert type(val1b) is str

        assert val1a == val1b

        val2 = self._conf.get_value_interp("archivestore", "path")
        assert val2 is not None
        assert type(val2) is str
        assert "%" not in val2



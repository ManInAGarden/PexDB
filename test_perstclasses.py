import unittest
from PersistClasses import *
from TestBase import *

class TestPrinterCrud(TestBase):

    def setUp(self):
        super().setUp()
    
    def test_printer_crud(self):
        #test create update delete of printer entities
        prin = Printer(name="testprinter", abbreviation="?TP?", firmware="Chitu", yearofbuild=2020)
        self.Spf.flush(prin)

    def test_extruder_crud(self):
        #test create update delete for extruder entities
        extr = Extruder(name="Qidi X-Plus HighTempAllMetal", abbreviation = "QIDIXPHTAM", maxtemperature=300, hascooler=False)
        self.Spf.flush(extr)

if __name__ == '__main__':
    unittest.main()



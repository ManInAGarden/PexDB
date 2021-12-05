import unittest
from PersistClasses import *
from TestBase import *
import sqlitepersist as sqp


class TestPrinterCrud(TestBase):

    def setUp(self):
        super().setUp()
    
    def test_printer_crud(self):
        #test create update delete of printer entities
        prin1 = self.Mck.create_printer(name="testprinter1", abbreviation="?TP?1", firmware="Chitu", yearofbuild=2020)
        prin2 = self.Mck.create_printer(name="testprinter2", abbreviation="?TP?2", firmware="Chitu", yearofbuild=2020)
        prin3 = self.Mck.create_printer(name="testprinter3", abbreviation="?TP?3", firmware="Chitu", yearofbuild=2020)

        q = sqp.SQQuery(self.Spf, Printer).where((Printer.Name=="testprinter1")
            & (Printer.Abbreviation=="?TP?1"))

        for sprin in q:
            assert(sprin is not None)
            assert(type(sprin) is Printer)
            assert(sprin.name == prin1.name and sprin.abbreviation==prin1.abbreviation)
            self.Spf.delete(sprin)
        

    def test_extruder_crud(self):
        #test create update delete for extruder entities
        extr = self.Mck.create_extruder(name="Qidi X-Plus HighTempAllMetal", abbreviation = "QIDIXPHTAM", maxtemperature=300, hascooler=False)
        #extr = Extruder(name="Qidi X-Plus HighTempAllMetal", abbreviation = "QIDIXPHTAM", maxtemperature=300, hascooler=False)
        self.Spf.flush(extr)

if __name__ == '__main__':
    unittest.main()



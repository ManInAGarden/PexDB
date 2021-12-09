import datetime as dt
import unittest
from PersistClasses import *
from TestBase import *
import sqlitepersist as sqp
from sqlitepersist.SQLitePersistBasicClasses import Catalog


class TestAllCrud(TestBase):

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

        prin1.name="Anderer Printer"
        self.Spf.flush(prin1)

        rprin1 = sqp.SQQuery(self.Spf, Printer).where(Printer.Id==prin1._id).first_or_default(None)
        assert(rprin1 is not None)
        assert(rprin1.name==prin1.name)
        

    def test_extruder_crud(self):
        #test create update delete for extruder entities
        extr = self.Mck.create_extruder(name="Qidi X-Plus HighTempAllMetal", abbreviation = "QIDIXPHTAM", maxtemperature=300, hascooler=False)

    def test_experiment_crud(self):
        #test create, update and delete for experiments
        dtn = dt.datetime(2020, 12, 6, 9, 30, 0)
        exp = self.Mck.create_experiment(carriedoutdt=dtn)

        expr = sqp.SQQuery(self.Spf, Experiment).where(Experiment.CarriedOutDt==dtn).first_or_default(None)
        assert(expr is not None)
        assert(expr.description==exp.description)
        assert(expr.printerusedid == exp.printerusedid)
        assert(expr.extruderusedid == exp.extruderusedid)
        #check for autofill embeds
        assert(expr.extruderused is not None)
        assert(type(expr.extruderused) is Extruder)
        assert(expr.printerused is not None)
        assert(type(expr.printerused) is Printer)

        #check for commanded embeds
        self.Spf.fill_joins(expr, Experiment.Settings)
        assert(expr.settings is not None)
        assert(type(expr.settings) is list)
        assert(len(expr.settings) == len(exp.settings))

    def test_parameter_crud(self):
        para = Parameter()
        para.name = "test"
        para.curaname = self.Spf.getcat(CuraNameCat, "MATERIAL_PRINT_TEMPERATURE") #has been seeded before, so should exist here
        self.Spf.flush(para)

        parar = sqp.SQQuery(self.Spf, Parameter).where(Parameter.Id==para._id).first_or_default(None)
        assert(parar is not None)
        assert(parar._id == para._id)
        assert(parar.curaname is not None)
        assert(type(parar.curaname) is CuraNameCat)
        assert(parar.curaname.code == "MATERIAL_PRINT_TEMPERATURE")





if __name__ == '__main__':
    unittest.main()



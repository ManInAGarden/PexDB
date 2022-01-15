from ast import excepthandler
import datetime as dt
import unittest
from uuid import uuid4
from PersistClasses import *
from TestBase import *
import sqlitepersist as sqp
from sqlitepersist.SQLitePersistBasicClasses import Catalog
from sqlitepersist.SQLitePersistQueryParts import SQQuery


class TestAllCrud(TestBase):

    def setUp(self):
        super().setUp()
    
    def test_printer_crud(self):
        #test create update delete of printer entities
        prin1 = self.Mck.create_printer(name="testprinter1", abbreviation="?TP?1", firmware="Chitu", yearofbuild=2020)
        prin2 = self.Mck.create_printer(name="testprinter2", abbreviation="?TP?2", firmware="Chitu", yearofbuild=2020)
        prin3 = self.Mck.create_printer(name="testprinter3", abbreviation="?TP?3", firmware="Chitu", yearofbuild=2020)

        q = sqp.SQQuery(self.Spf, Printer).where((Printer.Name=="testprinter1")
            & (Printer.Abbreviation==prin1.abbreviation))

        for sprin in q:
            assert(sprin is not None)
            assert(type(sprin) is Printer)
            assert(sprin.name == prin1.name and sprin.abbreviation==prin1.abbreviation)
            self.Spf.delete(sprin)

        prin2.name="Anderer Printer"
        self.Spf.flush(prin2)

        rprin2 = sqp.SQQuery(self.Spf, Printer).where(Printer.Id==prin2._id).first_or_default(None)
        assert(rprin2 is not None)
        assert(rprin2.name==prin2.name)
        

    def test_extruder_crud(self):
        #test create update delete for extruder entities
        extr = self.Mck.create_extruder(name="Qidi X-Plus HighTempAllMetal", abbreviation = "QIDIXPHTAM_x", maxtemperature=300, hascooler=False)

    def test_experiment_crud(self):
        #test create, update and delete for experiments
        dtn = dt.datetime(2020, 12, 6, 9, 30, 0)
        exp = self.Mck.create_experiment(carriedoutdt=dtn)

        expr = sqp.SQQuery(self.Spf, Experiment).where(Experiment.CarriedOutDt==dtn).first_or_default(None)
        assert(expr is not None)
        assert(expr.description==exp.description)
        assert(expr.printerusedid == exp.printerusedid)
        assert(expr.extruderusedid == exp.extruderusedid)
        assert(expr.isarchived == exp.isarchived)

        #check for autofill embeds
        assert(expr.extruderused is not None)
        assert(type(expr.extruderused) is Extruder)
        assert(expr.printerused is not None)
        assert(type(expr.printerused) is Printer)

        #check for commanded embeds
        self.Spf.fill_joins(expr, Experiment.Factors)
        assert(expr.factors is not None)
        assert(type(expr.factors) is list)
        assert(len(expr.factors) == len(exp.factors))

    def test_parameter_crud(self):
        para = FactorDefinition()
        para.name = "test"
        para.curaname = self.Spf.getcat(CuraNameCat, "MATERIAL_PRINT_TEMPERATURE") #has been seeded before, so should exist here
        self.Spf.flush(para)

        parar = sqp.SQQuery(self.Spf, FactorDefinition).where(FactorDefinition.Id==para._id).first_or_default(None)
        assert(parar is not None)
        assert(parar._id == para._id)
        assert(parar.curaname is not None)
        assert(type(parar.curaname) is CuraNameCat)
        assert(parar.curaname.code == "MATERIAL_PRINT_TEMPERATURE")

    def test_order_by(self):
        dtn1 = dt.datetime(2020, 12, 6, 9, 30, 0)
        exp = self.Mck.create_experiment(carriedoutdt=dtn1, description="OBTST")
        
        dtn2 = dt.datetime(2020, 12, 5, 9, 30, 0)
        exp = self.Mck.create_experiment(carriedoutdt=dtn2, description="OBTST")

        q = sqp.SQQuery(self.Spf, Experiment).where(Experiment.Description=="OBTST").order_by(Experiment.CarriedOutDt)
        oldcd = dt.datetime(1900, 1,1)
        for rexp in q:
            assert(oldcd < rexp.carriedoutdt)
            oldcd = rexp.carriedoutdt

    def test_experiment_doc(self):
        #special treatment becaus we know we have a on_after_delete in ExperimentDoc
        expdo = ExperimentDoc(name="QUARK", filepath="Nonexitent.zip")
        self.Spf.flush(expdo)

        assert expdo._id is not None

        rexpdo = sqp.SQQuery(self.Spf, ExperimentDoc).where(ExperimentDoc.Id == expdo._id).first_or_default(None)
        assert rexpdo is not None

        self.Spf.delete(rexpdo)
        r_rexpdo = sqp.SQQuery(self.Spf, ExperimentDoc).where(ExperimentDoc.Id == expdo._id).first_or_default(None)
        assert r_rexpdo is None

    def test_outer_transactions(self):
        self.Spf.begin_transaction("Testing transactions")
        try:
            pr = Printer(abbreviation=uuid4().hex, name="Transaction test printer")
            self.Spf.flush(pr)
            pr2 = sqp.SQQuery(self.Spf, Printer).where(Printer.Id==pr._id).first_or_default(None)
            assert pr2 is not None
            raise Exception("No real exception but a test of transactions")
            #we never get to this
            self.Spf.commit_transaction("useless commit")
        except:
            self.Spf.rollback_transaction("Testing transactions rollback")

        #now the new printer should be gone
        pr3 = sqp.SQQuery(self.Spf, Printer).where(Printer.Id==pr._id).first_or_default(None)
        assert pr3 is None


if __name__ == '__main__':
    unittest.main()



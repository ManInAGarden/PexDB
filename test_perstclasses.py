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

    def test_flat_cloning(self):
        prin = self.Mck.create_printer(name="testprinter1", firmware="Chitu", yearofbuild=2020)
        prinC = prin.clone()

        assert prin._id == prinC._id
        assert prin.name == prinC.name
        assert prin.abbreviation == prinC.abbreviation

    def test_updating(self):
        prin = self.Mck.create_printer(name="testprinter1", firmware="Chitu", yearofbuild=2020)
        self.Spf.flush(prin)
        newname = "changed name"
        prin.name=newname
        self.Spf.flush(prin)
        prin_r = sqp.SQQuery(self.Spf, Printer).where(Printer.Id==prin._id).first_or_default(None)
        assert prin_r is not None
        assert prin_r.name == newname

        newername = "name changed again"
        prin_r.name = newername
        self.Spf.flush(prin_r)
        prin_r_r = sqp.SQQuery(self.Spf, Printer).where(Printer.Id==prin._id).first_or_default(None) #remmeber id has not changed
        assert prin_r_r is not None
        assert prin_r_r.name == newername

    def test_deep_cloning(self):
        fpmock = {
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False}, #factorabbr : [min, max, levels]
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": True, "isnegated" : False, 
                "factorcombidefs" : ["PRINOZZTEMP", "PRISP"]},
            "PRISP" : {"minvalue": 40, "maxvalue": 60, "levelnum": 2, "iscombined": False}
        }

        proj = self.Mck.create_project()
        projC = proj.clone()
        assert proj._id == projC._id
        assert proj.status == projC.status #catalogs are immuteable, so the are not deeply cloned
        assert proj.status.code == projC.status.code

        #now we go deeper
        self.Mck.add_factor_preps(proj, fpmock)
        fpreps = list(sqp.SQQuery(self.Spf, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==proj._id))
        for fprep in fpreps:
            self.Spf.fill_joins(fprep, ProjectFactorPreparation.FactorCombiDefs) #fill to enable cloning on this
            fprepC = fprep.clone()
            assert len(fprepC.factorcombidefs) == len(fprep.factorcombidefs)
            for i in range(len(fprep.factorcombidefs)):
                fpcd = fprep.factorcombidefs[i]
                fpcdC = fprepC.factorcombidefs[i]
                assert fpcd.factordefinition.abbreviation == fpcdC.factordefinition.abbreviation

    
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

    def _get_facts_by_lst(self, abbrs : list):
        fdef_q = sqp.SQQuery(self.Spf, FactorDefinition).where(sqp.IsIn(FactorDefinition.Abbreviation, abbrs))
        answ = {}
        for fdef in fdef_q:
            answ[fdef.abbreviation] = fdef

        return answ

    def test_factcombipreps(self):
        myproj = self.Mck.create_project()
        fpreps = {
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False}, #factorabbr : [min, max, levels]
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": True, "isnegated" : False, 
                "factorcombidefs" : ["PRINOZZTEMP", "PRISP"]},
            "PRISP" : {"minvalue": 40, "maxvalue": 60, "levelnum": 2, "iscombined": False}
        }
        rpreps = {
            "DIMACC" : [1.0], #combination weight - deprecated, not used for anything!
            "SURFQUAL" : [1.0]
        }
        #get me the full info for the factor definitions
        fdict = self._get_facts_by_lst(list(fpreps.keys()))

        #add some factor- and response-preparations
        self.Mck.add_factor_preps(myproj, fpreps)
        self.Mck.add_response_preps(myproj, rpreps)

        fpreps_q = sqp.SQQuery(self.Spf, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==myproj._id)
        
        selpreps = list(filter(lambda fprep : fprep.factordefinition.abbreviation=="MATFLOW", fpreps_q))
        assert len(selpreps) == 1
        matflowprep = selpreps[0]
        assert matflowprep.iscombined
        self.Spf.fill_joins(matflowprep, ProjectFactorPreparation.FactorCombiDefs)
        assert matflowprep.factorcombidefs is not None
        assert len(matflowprep.factorcombidefs) == 2

        for fcdef in matflowprep.factorcombidefs:
            assert fcdef.factordefinition.abbreviation in ["PRINOZZTEMP", "PRISP"]

if __name__ == '__main__':
    unittest.main()



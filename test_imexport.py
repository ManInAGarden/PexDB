from csv import DictReader
from genericpath import exists
import unittest
import csv
from ExportImportProjects import ProjectExporter, ProjectImporter
from TestBase import *
import sqlitepersist as sqp

class TestImport(TestBase):
    def test_export(self):
        fpreps = {
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False},
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": False},
            "FANSPEED" : {"minvalue": 0, "maxvalue": 100, "levelnum": 2, "iscombined": True, "isnegated":False, 
                "factorcombidefs" : ["MATFLOW","PRINOZZTEMP"]}
        }
        rpreps = {
            "DIMACC" : [1.0], #combination weight - deprecated, not used for anything!
            "SURFQUAL" : [1.0]
        }
        epreps = {
            "CASETEMP" : {}
        }


        cnum, proj = self.Mck.create_fractfactorial_experiments(fpreps, 
            rpreps,
            epreps,
            projectname="test_simple_project")

        assert cnum == 4

        csvexp = ProjectExporter(self.Spf, proj)
        expfname = "testfiles/testexport.csv"
        
        csvexp.export_to_csv(expfname)
        
        #now check what we have...
        assert exists(expfname)
        with open(expfname, mode="r", encoding="UTF-8", newline="\n") as f:
            dreader = csv.DictReader(f)
            assert "EXP_SEQUENCE" in dreader.fieldnames
            assert "EXP_REPNUM" in dreader.fieldnames
            assert "EXP_DESCRIPTION" in dreader.fieldnames

            for name in fpreps:
                assert name in dreader.fieldnames

            for name in rpreps:
                assert name in dreader.fieldnames

            for name in epreps:
                assert name in dreader.fieldnames

            ct = 0
            for row in dreader:
                ct += 1

        assert ct == cnum


    def test_import(self):
        proj = self.Mck.create_project(name="ImportTestProject")

        #,,,DIMACC,SURFQUAL,CASETEMP
        fpreps_mck = {
            "PRINOZZTEMP": {"minvalue": 190, "maxvalue": 220, "levelnum": 2, "iscombined": False},
            "MATFLOW" : {"minvalue": 80, "maxvalue": 110, "levelnum": 2, "iscombined": False},
            "FANSPEED" : {"minvalue": 0, "maxvalue": 100, "levelnum": 2, "iscombined": True, "isnegated":False, 
                "factorcombidefs" : ["MATFLOW","PRINOZZTEMP"]}
        }
        rpreps_mck = {
            "DIMACC" : {"combinationweight" : 1.0}, #combination weight - deprecated, not used for anything!
            "SURFQUAL" : {"combinationweight" : 1.0}
        }
        epreps_mck = {
            "CASETEMP":{}
        }

        self.Mck.add_factor_preps(proj, fpreps_mck)
        self.Mck.add_response_preps(proj, rpreps_mck)
        self.Mck.add_enviro_preps(proj, epreps_mck)

        imp = ProjectImporter(self.Spf, proj)
        
        f_preps = sqp.SQQuery(self.Spf, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==proj._id).as_list()
        r_preps = sqp.SQQuery(self.Spf, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==proj._id).as_list()
        e_preps = sqp.SQQuery(self.Spf, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==proj._id).as_list()

        expfactn = len(f_preps)
        exprespn = len(r_preps)
        expenvn = len(e_preps)
        imp.import_from_csv("testfiles/testimport.csv")

        #now we should have experiments, factors, responeses, enviros
        exps = sqp.SQQuery(self.Spf, Experiment).where(Experiment.ProjectId==proj._id).as_list()
        for exp in exps:
            self.Spf.fill_joins(exp, 
                Experiment.Factors, 
                Experiment.Responses,
                Experiment.Enviros)

            assert len(exp.factors) == expfactn
            assert len(exp.responses) == exprespn
            assert len(exp.enviros) == expenvn


import unittest
from ExportImportProjects import ProjectImporter
from TestBase import *
import sqlitepersist as sqp

class TestImport(TestBase):
    def test_import(self):
        proj = self.Mck.create_project(name="ImportTestProject")
        imp = ProjectImporter(self.Spf, proj)
        f_preps = sqp.SQQuery(self.Spf, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==proj._id).as_list()
        r_preps = sqp.SQQuery(self.Spf, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==proj._id).as_list()
        e_preps = sqp.SQQuery(self.Spf, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==proj._id).as_list()

        expfactn = len(f_preps)
        exprespn = len(r_preps)
        expenvn = len(e_preps)
        imp.import_from_csv("./testfiles/Murksitest 2.csv")

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


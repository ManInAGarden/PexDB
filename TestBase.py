import unittest
import sqlitepersist as sqp
from  PersistClasses import *
import MockerParts as mocking
import json
from Properties import Properties

class TestBase(unittest.TestCase):

    Spf : sqp.SQFactory = None #the persitence factory
    Mck : mocking.Mocker = None #the Mocker-Factory
    PersTables = [sqp.PCatalog, sqp.CommonInter,
        Unit,
        FactorDefinition,
        FactorValue,
        ResponseDefinition,
        ResponseValue,
        EnviroDefinition,
        EnviroValue,
        Printer,
        Extruder,
        Experiment,
        ExperimentDoc,
        Project,
        ProjectFactorPreparation,
        ProjectResponsePreparation,
        ProjectEnviroPreparation,
        FactorCombiPreparation]

    @classmethod
    def setUpClass(cls):
        fact = sqp.SQFactory("PexDb", "PexDbTest.sqlite")
        fact.lang = "DEU"
        cls.Spf = fact
        fact.set_db_dbglevel("./sqpdebug.log", "DATAFILL") # use "STMTS for statements only or NONE for no sqlite-debugging at all"

        for tablec in cls.PersTables:
            cls.Spf.try_createtable(tablec)

        cls.Mck = mocking.Mocker(fact)
        try:
            sqp.SQPSeeder(fact, "./PexSeeds/catalogs.json").create_seeddata()
            sqp.SQPSeeder(fact, "./PexSeeds/units.json").create_seeddata()
            sqp.SQPSeeder(fact, "./PexSeeds/factordefinitions.json").create_seeddata()
            sqp.SQPSeeder(fact, "./PexSeeds/responsedefinitions.json").create_seeddata()
        except Exception as exc:
            print("Data seeding failed with {0}".format(str(exc)))


    @classmethod
    def tearDownClass(cls):
        q = 9 #breakpoint here to check db-contents before everything gets cleaned up after the test
        for tablec in cls.PersTables:
            cls.Spf.try_droptable(tablec)




import unittest
import sqlitepersist as sqp
from  PersistClasses import *
import MockerParts as mocking
import json
from Properties import Properties

class TestBase(unittest.TestCase):
    
    Spf : sqp.SQFactory = None #the persitence factory
    Mck : mocking.Mocker = None #the Mocker-Factory
    PersTables = [Unit, Parameter, Printer, Extruder, Setting, Experiment, sqp.PCatalog]
    
    @classmethod
    def setUpClass(cls):
        #cls.conf = Properties("./PexDb.conf")
        #url = cls.conf.dbconnection.url
        fact = sqp.SQFactory("PexDb", "PexDbTest.sqlite")
        fact.lang = "DEU"
        cls.Spf = fact
        
        for tablec in cls.PersTables:
            cls.Spf.try_createtable(tablec)

        cls.Mck = mocking.Mocker(fact)
        try:
            cls.Mck.create_seeddata("./PexSeeds/catalogs.json")
            cls.Mck.create_seeddata("./PexSeeds/units.json")
            cls.Mck.create_seeddata("./PexSeeds/parameters.json")
        except Exception as exc:
            print("Data seeding failed with {0}".format(str(exc)))


    @classmethod
    def tearDownClass(cls):
        q = 9 #breakpoint here to check db-contents before everything gets cleaned up after the test
        for tablec in cls.PersTables:
            cls.Spf.try_droptable(tablec)


    

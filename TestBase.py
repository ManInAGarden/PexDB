import unittest
import sqlitepersist as sqp
from  PersistClasses import *
import MockerParts as mocking
import json
from Properties import Properties

class TestBase(unittest.TestCase):
    
    Spf : sqp.SQFactory = None #the persitence factory
    Mck : mocking.Mocker = None #the Mocker-Factory

    @classmethod
    def setUpClass(cls):
        #cls.conf = Properties("./PexDb.conf")
        #url = cls.conf.dbconnection.url
        fact = sqp.SQFactory("PexDb", "PexDbTest.sqlite")
        fact.lang = "DEU"
        mock = mocking.Mocker(fact)
        #mock.create_seeddata("catseeds.json")
        cls.Mck = mock
        cls.Spf = fact
        
        cls.Spf.try_createtable(Printer())
        cls.Spf.try_createtable(Extruder())

    @classmethod
    def tearDownClass(cls):
        cls.Spf.try_droptable(Printer())
        cls.Spf.try_droptable(Extruder())


    

import unittest
import FinalApp
import os
import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure

class TestFinalApp(unittest.TestCase):
    def setUp(self):
        self.testTMDB = f'https://api.themoviedb.org/3/configuration?api_key={FinalApp.tmdb_api_key}'
        self.test_collection = FinalApp.db['favoriteMoviesTest']
        self.testData = {"test": "data"}

    def test_findCert(self):
        self.assertTrue(os.path.exists('./FinalProject.pem'))
        
    def test_Key(self):
        response = requests.get(self.testTMDB)
        self.assertTrue(response.status_code == 200)

    def test_createData(self):
        self.test_collection.insert_one(self.testData)
        self.doesExist = self.test_collection.find_one(self.testData)
        self.assertTrue(self.doesExist)

    def test_deleteData(self):
        self.test_collection.delete_one(self.testData)
        self.doesExist = self.test_collection.find_one(self.testData)
        self.assertFalse(self.doesExist)
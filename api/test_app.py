from unittest.mock import Mock
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult
from bson.objectid import ObjectId
import pymongo
import unittest
import flask
import app

class ApiTest(unittest.TestCase):
    ANIMALS_URL = 'http://localhost:5000/animais'

    def setUp(self) -> None:
        self.api = flask.Flask(__name__)
        
        self.db = app.db
        self.db = Mock()

        def find_one_side_effect():
            return {'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'}
        def insert_side_effect():
            insertresult = InsertOneResult(ObjectId('0123456789ab0123456789ab'),True)
            return insertresult
        def delete_side_effect():
            deleteresult = DeleteResult({'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'},True)
            return deleteresult
        def update_side_effect():
            updateresult = UpdateResult({'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'},True)
            return updateresult
        def find_side_effect():
            return [
                {'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'},
                {'date': "10-11-2019", 'name': "Mel", 'weight': 12, 'type': 'Cachorro'}
            ]
        
        self.db.animals.insert_one = Mock(side_effect=insert_side_effect) 
        self.db.animals.delete_one = Mock(side_effect=delete_side_effect)
        self.db.animals.find_one = Mock(side_effect=find_one_side_effect)
        self.db.animals.find = Mock(side_effect=find_side_effect)
        self.db.animals.update_one = Mock(side_effect=update_side_effect)

    # Http methods
    def test_get_all_animals_not_found(self):
        with self.api.test_client() as c:
            
            r = c.get(f"{ApiTest.ANIMALS_URL}")
            self.assertEqual(r.status_code, 404)

    # --- Database Mocks --- #
    def test_get_one_database(self):
        animalExpected = {'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'}
        animalQuery = self.db.animals.find_one()
        self.assertEqual(animalQuery, animalExpected)
        
    def test_get_all_database(self):
        animalExpected = [
                {'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'},
                {'date': "10-11-2019", 'name': "Mel", 'weight': 12, 'type': 'Cachorro'}
        ]
        animalQuery = list(self.db.animals.find())
        self.assertEqual(animalQuery, animalExpected)   

    def test_insert_one_database(self):
        animalQuery = self.db.animals.insert_one()
        self.assertEqual(str(animalQuery.inserted_id), '0123456789ab0123456789ab')
    
        

  

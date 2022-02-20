from unittest.mock import Mock
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult
from bson.objectid import ObjectId
from requests.models import Response
from werkzeug.wrappers import respose
from flask import request
import pymongo
import unittest
import flask
import app

class ApiTest(unittest.TestCase):
    animals = 'http://localhost:5000/animals'
    payload = {}
    payload['date']= "10-12-2010"
    payload['name']= "Lili"
    payload['type']= "Gato"
    payload['weight']= "10"

    def setUp(self):
        request.post(self.animals,json={'date': "10-11-2019", 'name': "anabelle", 'weight': 12, 'type': 'Cachorro'})
        request.post(self.animals,json={'date': "1-12-2015", 'name': "cabe", 'weight': 7, 'type': 'Gato'})
        self.object = (request.get(self.animals)).json()
        self.object_id = self.object[0]['_id']


    
    
        

  

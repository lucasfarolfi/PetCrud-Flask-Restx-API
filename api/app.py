# --- Imports and initial configs --- #
from flask import Flask, request
from flask_restx import Resource, Api
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)
api = Api(app)

# --- MongoDB config --- #
try:
    #Mongo Connection
    mongo = pymongo.MongoClient(
        host="localhost", 
        port=27017, 
        serverSelectionTimeoutMS = 1
    )

    db = mongo.company
    print("Database connected")
except:
    print("Error - Cannot connect to Database")

# --- Routes --- #
@api.route('/animais')
class Animals(Resource):
    #@api.marshal_list_with(lista, code=200, envelope="animals")
    def get(self):
        try:
            data = list(db.animals.find())
            for a in data:
                a["_id"] = str(a["_id"])
            
            return data, 200

        except Exception as ex:
            print(ex)
            return {
                "message": "Cannot get animals"
            }, 500
    
    #@api.marshal_list_with(code=200, envelope="animals")
    def post(self):
        try:
            data = request.get_json()
            aname = data.get("name")
            atype = data.get("type")
            aweight = data.get("weight")
            adate = data.get("date")
            newAnimal = {"name": aname, "type": atype, "weight": aweight, "date": adate}

            if aname == None or atype == None or aweight == None or adate == None:
                return {
                "message": "Invalid animal data"
                }, 403

            dbResponse = db.animals.insert_one(newAnimal)
            return {
                "message": "Animal created",
                "id": str(dbResponse.inserted_id)
            }, 201
        except Exception as ex:
            print(ex)
            return {
                "message": "Cannot create a animal"
            }, 500
        
@api.route('/animais/<string:animal_id>')
class Animal(Resource):
    def get(self,animal_id):
        try:
            data = db.animals.find_one({"_id": ObjectId(animal_id)})
            data["_id"] = str(data["_id"])

            return data, 200
        except Exception as ex:
            print(ex)
            return {
                "message": "Cannot get a animal"
            }, 500
    
    def put(self,animal_id):
        try:
            data = request.get_json()
            aname = data.get("name")
            atype = data.get("type")
            aweight = data.get("weight")
            adate = data.get("date")
            
            dbResponse = db.animals.update_one(
                {"_id": ObjectId(animal_id)},
                {"$set": {"name": aname, "type": atype, "weight": aweight, "date": adate}}
            )
            
            return {"message": "Animal updated","id": str(animal_id)}, 200
        except Exception as ex:
            print(ex)
            return {
                "message": "Cannot update a animal"
            }, 500
        
    def delete(self,animal_id):
        try:
            dbResponse = db.animals.delete_one({"_id": ObjectId(animal_id)})
            
            if dbResponse.deleted_count == 0:
                return {"message": "Animal not found"}, 404

            return {"message": "Animal deleted","id": str(animal_id)}, 200
        except Exception as ex:
            print(ex)
            return {
                "message": "Cannot delete a animal"
            }, 500


# Server configs and startup
if __name__ == '__main__':
    app.run(port=5000,debug=True)
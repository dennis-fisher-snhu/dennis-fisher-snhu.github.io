#!/usr/bin/python
import json
import bson
import bottle
from bottle import route, run, request, abort, post
from pymongo import MongoClient
import pymongo
from bson import json_util 
import datetime


connection = pymongo.MongoClient('localhost', 27017)
db = connection["market"]
collection = db["stocks"]

id = 0
# set up URI paths for REST service
@route('/greeting', methods=['POST', 'GET'])

def insert_document(document):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["city"]
        collection = db["inspections"]
        x = collection.insert_one(document)
        return True
    except Exception as ex:
        print(ex)
        return False
def get_document(document):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["city"]
        collection = db["inspections"]
        x = collection.find_one({ "business_name": document })
        print(x)
        return x
    except pymongo.errors.InvalidName: 
        print ("This document doesn't exist")
        return False
def update_document(idname, result):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["city"]
        collection = db["inspections"]
        #newValue = {"$set":{ "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 } }}
        #nv = { "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 }}
        #x = collection.update_one(document, newValue)
        #x = collection.find_one(nv)
        print(idname)
        print(result)
        x = collection.update({"id": idname},{ "$set": {"result": result}});
        print(x)
        return True
    except pymongo.errors.InvalidName: 
        return False
def delete_document(document):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["city"]
        collection = db["inspections"]

        collection.delete_many({ "id": document })
        x = collection.find_one({ "id": document })
        print(x)
        return True
    except pymongo.errors.InvalidName: 
        print ("This document doesn't exist")
        return False

if __name__ == '__main__': #declare instance of request
  #app.run(debug=True)
  run(host='localhost', port=8080)

#curl http://localhost:8080/update?id="10011-2017-TEST"&result="Violation%Issued"
#curl http://localhost:8080/delete?id="10011-2017-TEST"
#curl http://localhost:8080/read?business_name="ACME%TEST%INC."
#curl -H "Content-Type: application/json" -X POST -d '{"id" : "10011-2017-TEST","certificate_number" : 9278833,"business_name" : "ACME TEST INC.","date" : "Feb 20 2017","result" : "No Violation Issued","sector" : "Test Retail Dealer - 101"}' http://localhost:8080/create
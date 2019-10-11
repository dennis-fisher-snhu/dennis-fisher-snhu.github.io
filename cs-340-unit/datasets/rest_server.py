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
def get_greeting():
    global id
    id = id + 1
    try:
        request.query.name
        name=request.query.name
        if name: 
          #make calls to database from here
               string="{ \"id\": "+str(id)+", \"content\": \"Hello, \""+request.query.name+"\"}"
        else:
               string="{ \"id\": "+str(id)+", \"content\": \"Hello, World!\"}"
    except NameError:
        abort(404, 'No parameter for id %s' % id)

    if not string:
        abort(404, 'No id %s' % id)
    return json.loads(json.dumps(string, indent=4, default=json_util.default))
@route('/currentTime', methods=['POST', 'GET'])
def get_currentTime():
    dateString = datetime.datetime.now().strftime("%Y-%m-%d")
    timeString = datetime.datetime.now().strftime("%H:%M:%S")
    string="{\"date\":" + dateString + ",\"time\":" + timeString + "}"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))
  
@route('/hello', method='GET')
def get_hello():
    try:
        request.query.name
        name=request.query.name
        if name: 
          #make calls to database from here
               string="{ hello: \""+request.query.name+"\"}"
        else:
               string="{ \"content\": \"Hello, World!\"}"
    except NameError:
        abort(404, 'No parameter for id %s' % id)

    if not string:
        abort(404, 'No id %s' % id)
    return json.loads(json.dumps(string, indent=4, default=json_util.default))
@post('/strings')
def strings():
    print("called")
    if(request.method=="POST"):
        d = request.body.read().decode()
        d = eval(str(d))
        if("string1" in d):
            string = "{ first : \""+ d["string1"]+"\", second : \"" + d["string2"]+"\"}"
            if not string:
                abort(404, 'Failed to return')
            else:
                return json.loads(json.dumps(string, indent=4, default=json_util.default))
@post('/createStock')
def create():
    if(request.method=="POST"):
        d = request.body.read().decode()
        d = eval(str(d))
        if("Ticker" in d):
            doc1= { "Ticker" : d["Ticker"], "Volume" : d["Volume"], "Industry":d["Industry"],"Sector":d["Sector"],"50-Day Simple Moving Average":d["50-Day Simple Moving Average"]  }

            entity = insert_document(doc1)
            if not entity:
                abort(404, 'No document with business name %s' % d["business_name"])
            else:
                return json.dumps("Succesfully inserted")
@route('/getStock', methods=['POST', 'GET'])
def read():
    if(request.method=="GET"):
        #fixedname = request.query.business_name.replace("%"," ")
        fixedname = request.query.Ticker
        print(fixedname)
        entity = get_document(fixedname)
        if not entity:
            return json.dumps("document not found") 
        return json.dumps(str(entity)) 
@route('/updateStock', methods=['POST', 'GET'])
def update():
    if(request.method=="GET"):
        print(request.query.Ticker)
        print(request.query.Volume)
        print(request.body.read())
        entity = update_document(request.query.Ticker,request.query.Volume)
        if not entity:
            return json.dumps("document not found")
        print(entity)
        return json.dumps("document succesfully updated") 
@route('/deleteStock', methods=['POST', 'GET'])
def delete():
    if(request.method=="GET"):
        print(request.query.Ticker)
        entity = delete_document(request.query.Ticker)
        if not entity:
            return json.dumps("document does not exist") 
        return json.dumps("document succesfully deleted") 
def insert_document(document):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["market"]
        collection = db["stocks"]
        x = collection.insert_one(document)
        return True
    except Exception as ex:
        print(ex)
        return False
def get_document(document):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["market"]
        collection = db["stocks"]
        x = collection.find_one({ "Ticker": document })
        print(x)
        return x
    except pymongo.errors.InvalidName: 
        print ("This document doesn't exist")
        return False
def update_document(Tickername, volume):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["market"]
        collection = db["stocks"]
        #newValue = {"$set":{ "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 } }}
        #nv = { "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 }}
        #x = collection.update_one(document, newValue)
        #x = collection.find_one(nv)
        print(idname)
        print(result)
        x = collection.update({"Ticker": Tickername},{ "$set": {"Volume": volume}});
        print(x)
        return True
    except pymongo.errors.InvalidName: 
        return False
def update_doc(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["city"]
    collection = db["inspections"]
    
    newValue = {"$set":{"Ticker" : "ZZT", "Sector" : "Financial", "Change from Open" : -0.0154, "Performance (YTD)" : -0.2486, "Performance (Week)" : 0.0718, "Performance (Quarter)" : -0.1137, "200-Day Simple Moving Average" : -0.0346, "52-Week High" : -0.4275, "Change" : -0.032, "Volatility (Week)" : 0.0402, "Country" : "USA", "50-Day Low" : 0.1294, "Price" : 69.23, "50-Day High" : -0.314, "Industry" : "Exchange Traded Fund", "53-Week Low" : 0.3649, "Average True Range" : 2.59, "Company" : "Direxxion Daily Real Estate Bear 3X Shrs", "Gap" : -0.0179, "Relative Volume" : 1.56, "Volatility (Month)" : 0.0385, "Volume" : 507236, "Performance (Half Year)" : 0.2887, "Relative Strength Index (14)" : 54.78, "20-Day Simple Moving Average" : 0.01, "Performance (Month)" : 0.0272, "Performance (Year)" : -0.3548, "Average Volume" : 52.09, "50-Day Simple Moving Average" : -0.0208 }}
    nv = {"Ticker" : "ZZT", "Sector" : "Financial", "Change from Open" : -0.0154, "Performance (YTD)" : -0.2486, "Performance (Week)" : 0.0718, "Performance (Quarter)" : -0.1137, "200-Day Simple Moving Average" : -0.0346, "52-Week High" : -0.4275, "Change" : -0.032, "Volatility (Week)" : 0.0402, "Country" : "USA", "50-Day Low" : 0.1294, "Price" : 69.23, "50-Day High" : -0.314, "Industry" : "Exchange Traded Fund", "53-Week Low" : 0.3649, "Average True Range" : 2.59, "Company" : "Direxxion Daily Real Estate Bear 3X Shrs", "Gap" : -0.0179, "Relative Volume" : 1.56, "Volatility (Month)" : 0.0385, "Volume" : 507236, "Performance (Half Year)" : 0.2887, "Relative Strength Index (14)" : 54.78, "20-Day Simple Moving Average" : 0.01, "Performance (Month)" : 0.0272, "Performance (Year)" : -0.3548, "Average Volume" : 52.09, "50-Day Simple Moving Average" : -0.0208 }
    x = collection.update_one(document, newValue)
    x = collection.find_one(nv)
    print(x)

  except pymongo.errors.InvalidName: 
    print ("This document doesn't exist")
def delete_document(document):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        db = connection["market"]
        collection = db["stocks"]

        collection.delete_many({ "Ticker": document })
        x = collection.find_one({ "Ticker": document })
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
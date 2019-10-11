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
        fixedname = request.query.business_name.replace("%"," ")
        #fixedname = request.query.business_name
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
    
@route('/topFive', methods=['POST', 'GET'])
def topFive():
    if(request.method=="GET"):
        print(request.query.Industry)
        industry = request.query.Industry
        if(industry == None):
            return json.dumps("No Industry specified")
        else:
            industry = industry.replace("%20", " ")
            industry = industry.replace("%", " ")
            results = select_by_industry(industry)
            results.sort(key=sort_func)
            results.reverse()
            return json.dumps(results[0:5], default=json_util.default)
@post('/byTickers')
def byTickers():
    d = request.body.read().decode()
    print(d)
    d = eval(str(d))
    print(d)
    dic = {}
    for i in d["tickers"]:
        dic[i] = get_by_ticker(i)
    return json.dumps(dic, default=json_util.default)

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
    
def select_by_industry(industry):
    results = []
    cursor = collection.find( { "Industry":  industry } )
    for record in cursor:
        record.pop('_id', None)
        results.append(record)
    return results

#sorts documents by price
def sort_func(e):
    try:
        if(e.get("50-Day Simple Moving Average" != None)):
            return e["50-Day Simple Moving Average"]
        else:
            return e["Volume"]
    except:
        print(e)
        return -1

def select_by_min_max(minV, maxV):
    results = []
    cursor = collection.find( { "50-Day Simple Moving Average": { "$gt": minV , "$lt" : maxV} } )
    print("{:<14}{:<34}".format("Symbol", "50-Day Ave"))
    for record in cursor:
        results.append(record)
    return results

def get_by_ticker(ticker):
    cursor = collection.find( { "Ticker":  ticker } )
    dic = {}
    for record in cursor:
        dic = record
        dic.pop('_id', None)
    return dic
      
if __name__ == '__main__': #declare instance of request
  #app.run(debug=True)
  run(host='localhost', port=8080)


#curl http://localhost:8080/updateStock?Ticker="BRLI"&result="500"
#curl http://localhost:8080/delete?Ticker="BRLI"
#curl http://localhost:8080/getStock?Ticker="BRLI"
#curl -H "Content-Type: application/json" -X POST -d '{"Ticker" : ZTS, "Volume" : 500, "Industry":"Semiconductor Equipment & Materials","Sector":"Technology","50-Day Simple Moving Average":-0.0533 }' http://localhost:8080/createStock

#This curl as an example of how to test the top 5 peforming stocks in an industry
#   curl http://localhost:8080/topFive?Industry="Exchange%Traded%Fund"


#This curl as an example of how to test get stocks by list of tickers
#   curl -H "Content-Type: application/json" -X POST -d '{"tickers" : ["SNMX","TELK","PCLN","OXGN"]}' http://localhost:8080/byTickers
#
#curl -H "Content-Type: application/json" -X POST -d '{'Ticker': 'EEM', 'Sector': 'Financial', 'Change from Open': 0.0152, '200-Day Simple Moving Average': 0.0087, '52-Week High': -0.0735, 'Change': 0.0159, 'Volatility (Week)': 0.014, 'Country': 'USA', '50-Day Low': 0.065, 'Price': 41.45, '50-Day High': -0.056, 'Dividend Yield': 0.0181, 'Industry': 'Exchange Traded Fund', '52-Week Low': 0.1615, 'Average True Range': 0.54, 'Company': 'iShares MSCI Emerging Markets Index', 'Gap': 0.0007, 'Relative Volume': 1.07, 'Volume': '', 'Performance (Half Year)': -0.0438, '20-Day Simple Moving Average': -0.0212, 'Average Volume': 64990.81, '50-Day Simple Moving Average': -0.0126}' http://localhost:8080/createStock
      
#curl http://localhost:8080/deleteStock?Ticker="ATRS"
#curl http://localhost:8080/updateStock?Ticker="EEM"&Volume="4"
#curl http://localhost:8080/update?id="10011-2017-TEST"&result="Violation%Issued"
#curl http://localhost:8080/delete?id="10011-2017-TEST"
#curl http://localhost:8080/getStock?business_name="iShares%MSCI%Emerging%Markets%Index"

#curl http://localhost:8080/topFive?Industry="Exchange%Traded%Fund"
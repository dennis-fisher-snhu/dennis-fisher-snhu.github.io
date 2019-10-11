import pymongo
from bson import json_util
from pymongo import MongoClient

def insert_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["market"]
    collection = db["stocks"]
    x = collection.insert_one(document)
    return True
  except:
    return False
  
def get_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["market"]
    collection = db["stocks"]
    x = collection.find_one(document)
    print(x)
  except pymongo.errors.InvalidName: 
    print ("This document doesn't exist")
   
def update_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["market"]
    collection = db["stocks"]
    
    newValue = {"$set":{"Ticker" : "BRLI", "Sector" : "Financial", "Change from Open" : -0.0154, "Performance (YTD)" : -0.2486, "Performance (Week)" : 0.0718, "Performance (Quarter)" : -0.1137, "200-Day Simple Moving Average" : -0.0346, "52-Week High" : -0.4275, "Change" : -0.032, "Volatility (Week)" : 0.0402, "Country" : "USA", "50-Day Low" : 0.1294, "Price" : 69.23, "50-Day High" : -0.314, "Industry" : "Exchange Traded Fund", "53-Week Low" : 0.3649, "Average True Range" : 2.59, "Company" : "Direxxion Daily Real Estate Bear 3X Shrs", "Gap" : -0.0179, "Relative Volume" : 1.56, "Volatility (Month)" : 0.0385, "Volume" : 507236, "Performance (Half Year)" : 0.2887, "Relative Strength Index (14)" : 54.78, "20-Day Simple Moving Average" : 0.01, "Performance (Month)" : 0.0272, "Performance (Year)" : -0.3548, "Average Volume" : 52.09, "50-Day Simple Moving Average" : -0.0208 }}
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
    
    collection.delete_one(document)
    x = collection.find_one(document)
    print(x)
  except pymongo.errors.InvalidName: 
    print ("This document doesn't exist")
    
def main():
  doc1= { "Ticker" : "BRLI", "Sector" : "Financial", "Change from Open" : -0.0154, "Performance (YTD)" : -0.2486, "Performance (Week)" : 0.0718, "Performance (Quarter)" : -0.1137, "200-Day Simple Moving Average" : -0.0346, "52-Week High" : -0.4275, "Change" : -0.032, "Volatility (Week)" : 0.0401, "Country" : "USA", "50-Day Low" : 0.1594, "Price" : 60.23, "50-Day High" : -0.214, "Industry" : "Exchange Traded Fund", "52-Week Low" : 0.3349, "Average True Range" : 2.49, "Company" : "Direxion Daily Real Estate Bear 3X Shrs", "Gap" : -0.0169, "Relative Volume" : 1.06, "Volatility (Month)" : 0.0384, "Volume" : 50722, "Performance (Half Year)" : 0.2877, "Relative Strength Index (14)" : 54.68, "20-Day Simple Moving Average" : 0.06, "Performance (Month)" : 0.0262, "Performance (Year)" : -0.3538, "Average Volume" : 52.39, "50-Day Simple Moving Average" : -0.0207 }
  #doc2 = { "id" : "10021-2016-TEST", "certificate_number" : 9278808, "business_name" : "TEST INC.", "date" : "Feb 21 2017", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 } }
  #doc3 = { "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 }}

  print(insert_document(doc1))
  get_document(doc1)
  update_document(doc1)
  delete_document(doc1)   

  
main()
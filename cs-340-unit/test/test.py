import pymongo
from bson import json_util
from pymongo import MongoClient


def insert_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["city"]
    collection = db["inspections"]
    x = collection.insert_one(document)
    return True
  except:
    return False
  
def get_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["city"]
    collection = db["inspections"]
    x = collection.find_one(document)
    print(x)
  except pymongo.errors.InvalidName: 
    print ("This document doesn't exist")
   
def update_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["city"]
    collection = db["inspections"]
    
    newValue = {"$set":{ "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 } }}
    nv = { "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 }}
    x = collection.update_one(document, newValue)
    x = collection.find_one(nv)
    print(x)

  except pymongo.errors.InvalidName: 
    print ("This document doesn't exist")
 
def delete_document(document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection["city"]
    collection = db["inspections"]
    
    collection.delete_one(document)
    x = collection.find_one(document)
    print(x)
  except pymongo.errors.InvalidName: 
    print ("This document doesn't exist")
    

def main():
  doc1= { "id" : "10021-2015-TEST", "certificate_number" : 9278807, "business_name" : "TEST INC.", "date" : "Feb 20 2017", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 } }
  #doc2 = { "id" : "10021-2016-TEST", "certificate_number" : 9278808, "business_name" : "TEST INC.", "date" : "Feb 21 2017", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 } }
  #doc3 = { "id" : "10021-2017-TEST", "certificate_number" : 9278809, "business_name" : "TEST INC.", "date" : "June 2 2019", "result" : "No Violation Issued", "sector" : "TEST Retail Dealer - 127", "address" : { "city" : "RIDGEWOOD", "zip" : 11385, "street" : "MENAHAN ST", "number" : 5555 }}

  print(insert_document(doc1))
  get_document(doc1)
  update_document(doc1)
  delete_document(doc1)   

  
main()
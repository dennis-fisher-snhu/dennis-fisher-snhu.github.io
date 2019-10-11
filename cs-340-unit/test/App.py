import json
from pymongo import MongoClient
import pymongo
#3.

#open the connection
connection = pymongo.MongoClient('localhost', 27017)
db = connection["market"]
collection = db["stocks"]

#query for getting the values from the database
def getVals(minV, maxV):
    count = 0
    cursor = collection.find( { "50-Day Simple Moving Average": { "$gt": minV , "$lt" : maxV} } )
    print("{:<14}{:<34}".format("Symbol", "50-Day Ave"))
    for record in cursor:
        ave = record["50-Day Simple Moving Average"]
        symb = record["Ticker"]
        print("{:<14}{:<34}".format(symb, ave))
        count = count + 1
    print count
#retrive the minimum and maximum from the user
def get_min_max():
    minV = -1
    maxV = -1
    while(True):
        try:
            minV = float(input("Enter the minimum: "))
            maxV = float(input("Enter the maximum: "))
            if(minV < maxV):
                break
            else:
                print("The minimum must be less than the maximum")
        except:
            print("invalid input")
            continue
    return ((minV, maxV))

def select_by_industry(industry):
    results = []
    cursor = collection.find( { "Industry":  industry } )
    for record in cursor:
        results.append(record)
    return results

def select_by_sector(industry):
    results = []
    cursor = collection.find( { "Sector":  industry } )
    for record in cursor:
        results.append(record)
    return results

def display_sector(industry):
    results = select_by_sector(industry)
    results.sort(key=sort_func_industry)
    print("{:<14}{:<34}".format("Symbol", "Industry"))
    for result in results:
        print("{:<14}{:<34}".format(result["Ticker"], result["Industry"]))
        
def select_by_min_max(minV, maxV):
    count = 0
    results = []
    cursor = collection.find( { "50-Day Simple Moving Average": { "$gt": minV , "$lt" : maxV} } )
    print("{:<14}{:<34}".format("Symbol", "50-Day Ave"))
    for record in cursor:
        results.append(record)
        count = count + 1
        print count
    return results

def get_symbols_by_industry(industry):
    cursor = collection.find( { "Industry":  industry } )
    for record in cursor:
        symb = record["Ticker"]
        print(symb)
        
def get_by_ticker(ticker):
    cursor = collection.find( { "Ticker":  ticker } )
    dic = {}
    for record in cursor:
        dic = record
    return dic

#sorts documents by price
def sort_func(e):
    return e["50-Day Simple Moving Average"]
  
#sorts documents by price
def sort_func_industry(e):
    return e["Industry"]

def main():
    print("Select stocks with a 50-day simple moving average in a given range")
    vals = get_min_max()
    getVals(vals[0], vals[1])
    print("\n")
    print("Get symbol by industry")
    industry = str(input("Enter an industry (ex. Exchange Traded Fund): "))
    get_symbols_by_industry(industry)
    sector = str(input("Enter a Sector (ex. Healthcare): "))
    display_sector(sector)

if __name__ == '__main__':
    main()
    

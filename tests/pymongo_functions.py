import pymongo
import datetime
from datetime import date

import time
from datetime import datetime

def SendLineData(line,timestamp,day,stops_ids,rua):
    dic={}

    dic["day"] = day
    dic["time"] = timestamp
    dic["stop_id"]= stops_ids
    dic["rua"] = rua

    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017") # connect to mongo db

    db = myclient["Database_lines"] # acess the database

    line_col = db["Linha: "+str(line)]# get/create the collection

    x = line_col.insert_one(dic) # insert data
    

def SendBusData(bus_id,timestamp,day,possible_lines,paragem):
    # now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# SendBusData(50,current_time,date.today().strftime("%d/%m/%Y"),[1,2,6])
# time.sleep(1)
    dic={}
    dic["day"] = day
    dic["time"] = timestamp
    dic["bus_id"]= bus_id
    dic["paragem"] = paragem
    dic["possible_lines"] = possible_lines

    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017") # connect to mongo db

    db = myclient["Bus_lines"] # acess the database

    bus_col = db["Bus_Data: "+str(bus_id)]# get/create the collection
    #bus_col.drop()
    x = bus_col.insert_one(dic) # insert data
    
def updateBusData(bus_id,timestamp,day,possible_lines): 

    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    
    mydb = myclient["Bus_lines"]
    mycol = mydb["Bus_Data: "+ str(bus_id)]

    
    myquery = { "bus_id": bus_id}
    newvalues = { "$set": { 'possible_lines': [1,69] } }
    mycol.update_one(myquery, newvalues)
    #TODO
    myquery = { "time": timestamp}
    newvalues = { "$set": { 'time': timestamp } }
    mycol.update_one(myquery, newvalues)
    

    
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# updateBusData(50,current_time,date.today().strftime("%d/%m/%Y"),[2])
    
    
    
#!    TESTING  ------------------------------------------------------------------
# SendLineData(1,datetime.now(),date.today().strftime("%d/%m/%Y"),[123456789],"Rua Teste")
# time.sleep(1)
# SendLineData(1,datetime.now(),date.today().strftime("%d/%m/%Y"),[567890988],"Rua Teste2")


# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# SendBusData(50,current_time,date.today().strftime("%d/%m/%Y"),[1,2,6])
# time.sleep(1)

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# SendBusData(50,current_time,date.today().strftime("%d/%m/%Y"),[1])

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# SendBusData(51,current_time,date.today().strftime("%d/%m/%Y"),[1,2,9])
# time.sleep(1)

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# SendBusData(51,current_time,date.today().strftime("%d/%m/%Y"),[2])
#!--------------------------------------------------------------------------


def MapBoxTimeStampsPrediction(line,bus_id,stopAndTimestamp) :
    dic={}
    dic["Line"] = line
    dic["stopAndTimestamp"]= stopAndTimestamp

    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017") # connect to mongo db

    db = myclient["MapBoxTimeStampsPrediction"] # acess the database

    bus_col = db["Bus_Id: "+ str(bus_id)]# get/create the collection

    x = bus_col.insert_one(dic) # insert data
    
# prediçao1 = (123,datetime.now().strftime("%H:%M:%S"))
# MapBoxTimeStampsPrediction(7,50,prediçao1)
# time.sleep(1)
# prediçao2 = (321,datetime.now().strftime("%H:%M:%S"))
# MapBoxTimeStampsPrediction(7,50,prediçao2)

#drop pymongo
def dropDatabases(lines,bus_lines,mapBoxTimeStampsPrediction): # delete databases fucntions lines,bus_lines,mapBoxTimeStampsPrediction
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017") # connect to mongo db
    if lines:
        myclient.drop_database("Database_lines")
    if bus_lines:
        myclient.drop_database("Bus_lines")
    if mapBoxTimeStampsPrediction:
        myclient.drop_database("MapBoxTimeStampsPrediction")

#dropDatabases(True,True,True)

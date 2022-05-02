import pymongo
import datetime
from datetime import date

import time
from datetime import datetime

def SendLineData(line,timestamp,day,stops_ids):
    dic={}

    dic["day"] = day
    dic["time"] = timestamp
    dic["stop_id"]= stops_ids

    myclient = pymongo.MongoClient("mongodb://localhost:27017/") # connect to mongo db

    db = myclient["Database_lines"] # acess the database

    line_col = db["Linha: "+str(line)]# get/create the collection

    x = line_col.insert_one(dic) # insert data
    

def SendBusData(bus_id,timestamp,day,possible_lines):
    
    dic={}
    dic["day"] = day
    dic["time"] = timestamp
    dic["bus_id"]= bus_id
    dic["possible_lines"] = possible_lines

    myclient = pymongo.MongoClient("mongodb://localhost:27017/") # connect to mongo db

    db = myclient["Bus_lines"] # acess the database

    bus_col = db["Bus_Data: "+str(bus_id)]# get/create the collection

    x = bus_col.insert_one(dic) # insert data
    
    
#    TESTING 
# SendLineData(1,datetime.now(),date.today().strftime("%d/%m/%Y"),[123,245,35678])
# time.sleep(1)
# SendLineData(1,datetime.now(),date.today().strftime("%d/%m/%Y"),[123,245,35678,12345,987654,456789])


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


def MapBoxTimeStampsPrediction(line,bus_id,stopAndTimestamp) :
    dic={}
    dic["Line"] = line
    dic["stopAndTimestamp"]= stopAndTimestamp

    myclient = pymongo.MongoClient("mongodb://localhost:27017/") # connect to mongo db

    db = myclient["MapBoxTimeStampsPrediction"] # acess the database

    bus_col = db["Bus_Id: "+ str(bus_id)]# get/create the collection

    x = bus_col.insert_one(dic) # insert data
    
# prediçao1 = (123,datetime.now().strftime("%H:%M:%S"))
# MapBoxTimeStampsPrediction(7,50,prediçao1)
# time.sleep(1)
# prediçao2 = (321,datetime.now().strftime("%H:%M:%S"))
# MapBoxTimeStampsPrediction(7,50,prediçao2)


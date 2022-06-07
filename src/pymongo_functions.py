import pymongo
import datetime
from datetime import date

import time
from datetime import datetime

import json
import requests

myclient = pymongo.MongoClient("mongodb://mongo:27017") # connect to mongo db
    

def SendBusData(bus_id,timestamp,day,possible_lines,paragem,prediction):
    """
    
    | This function sends the line,day,timestamp,stop and next stop time predictions to the mongodb local database
    
    .. note::
        * the mondo db is locally instantiated : mongodb://localhost:27017

    Args:
        bus_id (int): the bus id
        timestamp (str): Timestamp appearance of the bus in the OBU
        day (str): Day of the detection
        possible_lines (list): the possible line(s) that the bus can go
        paragem (str): Last stop found of the detected line witht he highest confidence
        prediction (list): The next estimated time of the arrival of the bus to its next stops in the line
        
    """
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # SendBusData(50,current_time,date.today().strftime("%d/%m/%Y"),[1,2,6])
    # time.sleep(1)
    dic={}
    dic["day"] = day
    dic["time"] = timestamp
    dic["bus_id"]= bus_id
    dic["paragem"] = paragem
    dic["line"] = possible_lines
    dic["prediction"] = {}
    dic["prediction"] = prediction
    
    
    payload = json.dumps({
    "id": "urn:ngsi-ld:Bus:peci_bus:"+bus_id,
    "type": "Bus",
    "dateSent": {
        "type": "DateTime",
        "value": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    },
    "busData":{
        "type": "dict",
        "value": dic
    }
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlIjoicGVjaV9idXMiLCJpYXQiOjE2NDk3MTIyMjJ9.MnKA5nJ8XOEtSWbW9lcWLnhdejcWGQMz07WxTsH0Pk4',
    'Fiware-service': 'peci_bus'
    }

    r = requests.post('https://orion.atcll-data.nap.av.it.pt/v2/entities?options=upsert' ,data=payload, headers=headers)

    print(r.status_code==204)


    db = myclient["Bus_lines"] # acess the database

    bus_col = db["Bus_Data: "+str(bus_id)]# get/create the collection
    #bus_col.drop()
    bus_col.insert_one(dic) # insert data

   
    
def getBusData(bus_id):
    """
    
    | This function gets the information stored in the mongodb local database of a selected bus.
    | It is used for the app to get the information of the bus.
    
    .. note::
        * the mondo db is locally instantiated : mongodb://localhost:27017

    Args:
        bus_id (int): the bus id
        
    :return: Dictionary with the information about the bus and its predictions.
    :rtype: dict
        
    """

    db = myclient["Bus_lines"] # acess the database

    bus_col = db["Bus_Data: "+str(bus_id)]# get/create the collection
    
    return bus_col.find_one()


# def updateBusData(bus_id,timestamp,day,possible_lines): 

#     myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    
#     mydb = myclient["Bus_lines"]
#     mycol = mydb["Bus_Data: "+ str(bus_id)]

    
#     myquery = { "bus_id": bus_id}
#     newvalues = { "$set": { 'possible_lines': [1,69] } }
#     mycol.update_one(myquery, newvalues)
#     #TODO
#     myquery = { "time": timestamp}
#     newvalues = { "$set": { 'time': timestamp } }
#     mycol.update_one(myquery, newvalues)
    

    
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


def MapBoxTimeStampsPrediction(line,bus_id,stop,timeStamp) :
    """
    
    | This function is used to save everything that the line detection does.
    
    .. note::
        * the mondo db is locally instantiated : mongodb://localhost:27017

    Args:
        line (int): the detected line
        bus_id (int): the bus id
        stop (str): the last detetcted stop of the line
        timeStamp (str): the timestamp of the detection
        
    """
    
    dic={}
        
    dic['date']= str(datetime.now().strftime("%d/%m/%Y"))
 
    dic['time'] = datetime.now().strftime("%H:%M:%S")
    dic['bus_id'] = bus_id
    dic["Line"] = line
    dic["Stop"]= stop
    dic["timeStamps"] = timeStamp
    


    db = myclient["MapBoxTimeStampsPrediction"] # acess the database

    bus_col = db["Bus_Id: "+ str(bus_id)]# get/create the collection

    bus_col.insert_one(dic) # insert data


    
# prediçao1 = (123,datetime.now().strftime("%H:%M:%S"))
# MapBoxTimeStampsPrediction(7,50,prediçao1)
# time.sleep(1)
# prediçao2 = (321,datetime.now().strftime("%H:%M:%S"))
# MapBoxTimeStampsPrediction(7,50,prediçao2)

#drop pymongo

def LinesData(line,bus_id,stop) :
    
    dic={}
    dic['date']= str(datetime.now().strftime("%d/%m/%Y"))
    dic['time'] = datetime.now().strftime("%H:%M:%S")
    dic['bus_id']= bus_id
    dic['stop']= stop
    
    db = myclient["LinesData"] # acess the database
    
    bus_col=db[str(line)]
    
    bus_col.insert_one(dic)


def dropDatabases(bus_lines,mapBoxTimeStampsPrediction): # delete databases fucntions lines,bus_lines,mapBoxTimeStampsPrediction
    """
    
    | This function is used to delete the databases
    
    .. note::
        * the mondo db is locally instantiated : mongodb://localhost:27017

    Args:
        bus_lines (bool): the name of the database
        mapBoxTimeStampsPrediction (bool): the name of the database
        
    """
    print(type(bus_lines))
    
    if bus_lines:
        myclient.drop_database("Bus_lines")
    if mapBoxTimeStampsPrediction:
        myclient.drop_database("MapBoxTimeStampsPrediction")

#dropDatabases(True,True)
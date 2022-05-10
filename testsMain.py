import json
import time
import distance as dist
from tests import pymongo_functions
import paho.mqtt.client as mqtt
from datetime import datetime
from datetime import date

from tests import pymongo_functions

bus_list = {}


#TESTE---------------------
#!working---------------------------------
# temp = autocarro.copy()
# temp['id'] = 1
# temp['linhas'] = [1,2,3]
# bus_list.append(temp)

# temp = autocarro.copy()
# temp['id'] = 2
# temp['linhas'] = [3,4,5]
# bus_list.append(temp)

# print("Autocarro_lista: ", bus_list)
#!----------------------------------------
#bus_list[0]=[1,2,3,4,5,6,7,8,9,10,11,12,13]

#bus_list[50]=[1,2,3,4,5,6,7,8,9,10,11,12,13]



#!REAL DATA---------------------

received_data=[] # receber data por mqtt

file=open('json/stops per line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')

file=open('json/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')

file=open('json/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')

file=open('json/stops.json', mode="r")
ends_of_line = json.load(file, encoding='utf-8')
#!--------------------------------------

#!DUMMY DATA -----------------------------------
# file=open('Dummy/DummyStop_per_line.json', mode="r")
# stops_of_line = json.load(file, encoding='utf-8')

# file=open('Dummy/DummyLines_per_stop.json', mode="r")
# lines_of_stop = json.load(file, encoding='utf-8')

# file=open('Dummy/DummyStops.json', mode="r")
# stops = json.load(file, encoding='utf-8')

#!----------------------------------------------


def getLinesOfStop(stop_id):  #*WORKING
    for stop in lines_of_stop:
        if str(stop_id) == stop:
            return lines_of_stop[stop]['lines'] #!Index 1 is the name of the stop
        

def ParagemUnica(paragem): # give stop and return if its the only stop in its line
    paragem= str(paragem) #* WORKING
    for stop in lines_of_stop:
        if paragem == stop and len(lines_of_stop[stop]['lines']) == 1:
            return True
    return False

def checkStop(coordenadas): # check if a stop is nearby
    candidates=[]
    for stop in stops: #* WORKING
        tuple = dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.1) # 0.2 km is the range to check
        if tuple[0] : 
            candidates.append((stop, tuple[1])) if stop not in candidates else candidates 
        #return min of a tuple in the second argument and default value if there is no tuple
    paragem=min(candidates, key=lambda x: x[1])[0] if candidates else 0
    print("paragem -- " ,stops[str(paragem)]['name'])
    return  paragem #!ID 0 means no stop is nearby
   

def Analise_stop(bus_id,paragem): # from the id of the bus and the stop number, change the saved lines of 
                                # that bus so that it coincides with the lines of the stop that that bus passed through 
                                # ex : saved : [1,2,3,4]
                                # new : [4,5]
                                # change to : [4]
                                
    #!DISCLAIMER:
    #When i did this only I and God knew how it worked, now only God knows
    
    stops_of_line = getLinesOfStop(paragem) # return the lines that pass through the stop
    possible_lines = [] # array para guardar as linhas possiveis
   
    for line in stops_of_line: 
        for linha_guardada in bus_list[bus_id]: 
            if line == linha_guardada : # ha aqui u problema com as linhas que nao existem no json 
                possible_lines.append(line)
                
    bus_list[bus_id] = possible_lines # guarda as linhas possiveis
    return possible_lines# atualizacao das linhas possiveis
    
def Find_line_of_bus(bus, bus_id): #*TODO Find line(s) of bus by ID
    temp={}
    #bus_id = 50
    if bus_id not in bus_list.keys():
        bus_list[bus_id] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    #check if id in dictionary
    for time in bus[bus_id]['data']:
        print("len:",len(bus_list[bus_id]))
        if(len(bus_list[bus_id])==0):
            bus_list[bus_id] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            print("a")
        if(len(bus_list[bus_id])==1):
            temp= [1,2,3,4,5,6,7,8,9,10,11,12,13]
            print("a") 
        print(time)
        #for coord in bus['data'][time]: # para cada paragem que esta no historico da OBU
        print(bus_list)
        coord =(bus[bus_id]['data'][time]['coords']['lat'], bus[bus_id]['data'][time]['coords']['long'])
        possible_lines={}
    
        paragem = checkStop(coord) # verificar se a paragem existe e devolve o ID dela 
        if paragem == 0:   
            continue 
        else:
            if ParagemUnica(paragem):
                bus_list[bus_id] = getLinesOfStop(paragem) # receber a linha da paragem (vai se so uma)
                #print("unga bunga")
                #return
            else:
                
                possible_lines = Analise_stop(bus_id,paragem) # compar com as linas possiveis obtidas anteriormente 
                                                                # com as linhas possiveis novas                                                                
                if(len(bus_list[bus_id])==1):
                    print("linha unica")
                #     #TODO send linha á app
                
        pymongo_functions.SendBusData(bus_id,list(bus[bus_id]['data'].keys())[-1],date.today().strftime("%d/%m/%Y"),possible_lines,paragem)

    #else: # autocarro novo

     #       for coordenada in received_data.autocarro.coordenadas: # para cada paragem que esta no historico da OBU
      #          paragem = checkStop(coordenada) # verificar se a paragem existe e devolve o ID dela 
       #         bus[id_bus] = getLinesOfStop(paragem) # receber a(s) linha(s) da paragem 


    # #TODO send linha á app /done
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    pymongo_functions.SendBusData(bus_id,current_time,date.today().strftime("%d/%m/%Y"),bus_list[bus_id],paragem)
    

# def Line_detection():
#     while(True):

#         receiver = connect_mqtt()
#         receiver.loop_start()
#         publish(receiver)

#         #when a new bus appears in real-time
#         #get history of the last hour 

#         for autocarro in received_data[autocarro]: # processar os dados autocarro a autocarro
#             Find_line_of_bus(autocarro) # descobrir se possível a linha do autocarro e avisar a aplicação mobile

#         time.sleep(1)



def filterData(bus):
    temp = {}
    
    for time in bus['data']:
        coord =(bus['data'][time]['coords']['lat'], bus['data'][time]['coords']['long'])
        paragem = checkStop(coord) # verificar se a paragem existe e devolve o ID dela 
        if paragem in ends_of_line.keys():
            #TODO
            temp.clear()
        else:
            temp[time] = bus['data'][time]
    return temp
    
def Line_detection(bus):

    #TODO bus_filter = filterData(bus)
    Find_line_of_bus(bus,list(bus.keys())[0]) # descobrir se possível a linha do autocarro e avisar a aplicação mobile
        
#TODO ver a posiçao do autocarro mais recente ver a linha que deu e com isso
# TODOandar para tras no array de fins meios e inicos de linha e detetar o sentido
#----------------------------------------------------------------------------------------------------------
# python 3.6

import time
import json
import datetime
from datetime import timedelta
import requests
import pprint
from dateutil import tz

import paho.mqtt.client as mqtt

import socket
import signal
import sys



#! ------------------------- ORION HISTORY -------------------------

# * credentials for the API
user_and_password = '{"username": "peci_2122_atcll","password": "pecII_2122_atcll+"}'
headers = {"Content-type": "application/json", "Accept-Charset": "UTF-8"}

# * array to select the services and types
services = ["aveiro_cam", "aveiro_radar", "transdev"]
types = ["Traffic", "Count", "Values"]

# * Create ORION Auth Token
def get_api_authtoken():
    res = requests.post(
        "https://api.atcll-data.nap.av.it.pt/auth",
        data=user_and_password,
        headers=headers,
    )
    if res.status_code == 200:
        return res.headers.get("authorization")

    print("Token is missing!!")
    print(res.text)


# * Makes the URL to get the historical data from the API
# * Receives the start and end time in milliseconds
def make_history_url(start_time, end_time):
    return (
        "https://api.atcll-data.nap.av.it.pt/history?type=obugps&start="
        + str(start_time)
        + "&end="
        + str(end_time)
        + "&attribute=location"
    )


# * Makes the historical request to the API
# * Receives the token and the url and the service to subscribe
def get_history_request(token, url, service):
    r = requests.get(url, headers={"FIWARE-Service": service, "authorization": token})

    try:
        if r.json():
            print("REQUEST SUCESSEFULL")
            return r.json()
        else:
            print("NO DATA")
            return {}

    except:
        print(r.text)
        return {}


# * Converts a datetime date to milliseconds
def date_to_millisecconds(date):
    return int(time.mktime(date.timetuple()) * 1000)


# * Get all the keys of the dictionary
# * retuns the list of keys sorted
def get_key_Values(dictionary):
    keylist = list(dictionary.keys())
    keylist.sort()
    return keylist


# * Fix the time in the json from GMT to local time
def json_fix_time(json):
    from_zone = tz.gettz("GMT")
    to_zone = tz.gettz("Europe/London")
    # *gets all buses in the json
    # * bus=  urn:ngsi-ld:obuGPS:transdev:50 where 50 is the bus number
    for bus in get_key_Values(json):
        i = 0
        for GMTtime in json[bus]["time_index"]:
            # * GMTtime = 2022-03-30T08:25:51
            tmp = GMTtime.split("T")

            tmpDate = tmp[0]
            tmpTime = tmp[1]

            splitDate = tmpDate.split("-")
            splitTime = tmpTime.split(":")

            # * puts the time_index date to datetime format
            datetimeGMT = datetime.datetime(
                int(splitDate[0]),
                int(splitDate[1]),
                int(splitDate[2]),
                int(splitTime[0]),
                int(splitTime[1]),
                int(splitTime[2]),
                0,
            )

            # * change the timezone
            datetimeGMT = datetimeGMT.replace(tzinfo=from_zone)
            datetimeLocal = datetimeGMT.astimezone(to_zone)

            # * puts the new time in the correct format
            newTime = (
                str(datetimeLocal.year)
                + "-"
                + "{:02d}".format(datetimeLocal.month)
                + "-"
                + "{:02d}".format(datetimeLocal.day)
                + "T"
                + "{:02d}".format(datetimeLocal.hour)
                + ":"
                + "{:02d}".format(datetimeLocal.minute)
                + ":"
                + "{:02d}".format(datetimeLocal.second)
            )

            # * replaces the old time with the new one
            json[bus]["time_index"][i] = newTime
            i += 1


# * function to handle the AI request
def make_IA_request(stationID):
    # * get the token
    token = get_api_authtoken()

    # * get the start and end time
    # * when this function is called, the end time is the current time
    dStart = datetime.datetime(2022, 5, 9, 18, 0)
    dEnd = datetime.datetime(2022, 5, 9, 19, 0)
    
    #dEnd = datetime.datetime.now() 
    #dStart = dEnd - datetime.timedelta(minutes=60)

    # * convert the start and end time to milliseconds
    start_time = date_to_millisecconds(dStart)
    end_time = date_to_millisecconds(dEnd)

    # * make the url to get the data from the API
    url = make_history_url(start_time, end_time)

    # * make the request to the API
    requestJSON = get_history_request(token, url, services[2])

    
    # * if the json is empty that means no data was found for the time period
    # * puts in mqtt an empty array
    if requestJSON == {}:
        return {}
    # * if the json is not empty, fix the time and put the json in mqtt
    else:
        json_fix_time(requestJSON)
        cleanJSON = format_json(requestJSON,stationID)
        return cleanJSON


# * Function to format the json for the AI request
def format_json(jsonn,stationID):
    formatedJSON = {}
    # * gets all buses in the json
    for fullBusID in get_key_Values(jsonn):
        # * fullBusID = urn:ngsi-ld:obuGPS:transdev:50 where 50 is the bus number
        splitBusID = fullBusID.split(":")
        busID = int(splitBusID[4])
        if stationID== busID:
            formatedJSON[str(busID)] = {}
            formatedJSON[str(busID)]["data"] = {}

            # * puts in the formatedJSON the data for the bus by its time index
            for value in range(len((jsonn[fullBusID]["time_index"]))):
                if(int(jsonn[fullBusID]["time_index"][value].split("T")[1].split(":")[2]) % 10==0):
                    formatedJSON[str(busID)]["data"][
                        jsonn[fullBusID]["time_index"][value].split("T")[1]
                    ] = {
                        "coords": {
                            "lat": jsonn[fullBusID]["lat"][value],
                            "long": jsonn[fullBusID]["long"][value],
                        }
                    }
    return formatedJSON

#! ------------------------- REAL TIME -------------------------

MQTT_TOPIC = [("+/apu/cam",0)]

global y
y={}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
    


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    j_son = json.loads(msg.payload)
    if j_son["stationType"]==6: # Station Type (6) significa que é um autocarro
        if j_son["stationID"] in y.keys(): #se o autocarro está no dicionário significa que já passou por um poste
            if j_son["receiverID"] in y[j_son["stationID"]].keys(): # se o autocarro já passou neste poste
            # comparar o timestamp do ultimo poste e o timestamp do poste atual
                if j_son["timestamp"] > y[j_son["stationID"]][j_son["receiverID"]]: # se o timestamp do poste atual é maior que o timestamp do ultimo poste sigifica que o autocarro ainda está a passar no poste
                    y[j_son["stationID"]][j_son["receiverID"]] = j_son["timestamp"] # atualizar o timestamp do ultimo poste
                
            else: # é a primeira vez que o autocarro passa no poste
                IAjson=make_IA_request(int(j_son["stationID"]))
                print("IAjson: ",IAjson)
                Line_detection(IAjson)
                y[j_son["stationID"]][j_son["receiverID"]] = j_son["timestamp"]
        else: # é a primeira vez que o autocarro entra
            IAjson=make_IA_request(int(j_son["stationID"]))
            print("IAjson: ",IAjson)
            Line_detection(IAjson)
            y[j_son["stationID"]] = {}
            y[j_son["stationID"]][j_son["receiverID"]] = j_son["timestamp"]
            print(y)
    
    y_copy = {**y}
    stationList = list(y.keys())
    for station in stationList:
        l = list(y_copy[station].keys())
        for receiverIDkey in l:
            if (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(y[station][receiverIDkey])).total_seconds()> 60:
                print("del")
                print(y)
                print()
                del y[station][receiverIDkey]
    

def connect_mqtt():
    # criar variavel para receber os dados
    receiver = mqtt.Client()
    receiver.on_connect = on_connect
    receiver.on_message = on_message
    receiver.connect_async("atcll-data.nap.av.it.pt", 1884, 60)
    
    return receiver


#! ------------------------- ORION POST -------------------------

#* Posts the Line Detection json to the API 
#* Receives the json to post
def post_json_to_orion(LDjson):
    
    payload = json.dumps(LDjson)
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlIjoicGVjaV9idXMiLCJpYXQiOjE2NDk3MTIyMjJ9.MnKA5nJ8XOEtSWbW9lcWLnhdejcWGQMz07WxTsH0Pk4',
    'Fiware-service': 'peci_bus'
    }

    r = requests.post('https://orion.atcll-data.nap.av.it.pt/v2/entities?options=upsert' ,data=payload, headers=headers)
    
    if(r.status_code==204):
        print("Post successful")



#! ------------------------- MAIN -------------------------


if __name__ == "__main__":
    try:
        receiver = connect_mqtt()
        receiver.loop_forever()
            
    except KeyboardInterrupt:
        print("\r  ")
        print("Exiting Program...")
#----------------------------------------------------------------------------------------------------------

#if __name__ == "__Line_detection__":
#Line_detection()

#Find_line_of_bus(bus,50)
#print(bus_list)



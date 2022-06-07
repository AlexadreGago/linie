import json
import time

from regex import B
import distance as dist
import pymongo_functions
import paho.mqtt.client as mqtt
from datetime import datetime
from datetime import date
import ETAmapbox as ETAmapbox


#!IMPORTS SILVEIRA

import datetime
import requests
import pprint
from dateutil import tz
import socket
import signal
import sys
currenttimestamp=""
bus_list = {}

ends_turns= {1: (4873436913, 1364747314, 4873436913), #1
             2: (4873436915, 5403604506, 5398020251), #2
             3: (4873436913, 1364747314, 4873436913), #3
             4: (5401229911, 1364747314, 5401229910), #4
             5: (5398378854, 1364747314, -1), #5 # this line end had to be eliminated as it would cause conflicts
             6: (5395534183, 1364747314, 5395534182), #6
             8: (5410260321, 5398378854, 5410260321), #8
             10:(5410259987, 5398378854, 5410259986), #10
             11:(1699701236, -1, -1), #11 #this line end had to be eliminated as it would cause conflicts
             12:(5410259987, 5405326919, 5410259986), #12
             13:(5407623407, 4852088188, 1799461738)} #13
            # Start     ,  Turn     ,   End
            
ends_turns2= {1: (4873436913, 1364747314, 4873436913), #1
             2: (4873436915, 5403604506, 5398020251), #2
             3: (4873436913, 1364747314, 4873436913), #3
             4: (5401229911, 1364747314, 5401229910), #4
             5: (5398378854, 1364747314, 5398378854), #5
             6: (5395534183, 1364747314, 5395534182), #6
             8: (5410260321, 5398378854, 5410260321), #8
             10:(5410259987, 5398378854, 5410259986), #10
             11:(1699701236, 0000000000, 4852045631), #11
             12:(5410259987, 5405326919, 5410259986), #12
             13:(5407623407, 4852088188, 1799461738)} #13
            # Start     ,  Turn     ,   End
            
line_ends= list(map (lambda x:(x[2]),ends_turns.values()))
            
#!REAL DATA---------------------

received_data=[] # receber data por mqtt

file=open('../json/stops per line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')

file=open('../json/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')

file=open('../json/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')

file=open('../json/stops.json', mode="r")
ends_of_line = json.load(file, encoding='utf-8')

file=open('../json/message.json', mode="r")
realbusdata = json.load(file, encoding='utf-8')

file=open('../json/message2.json', mode="r")
realbusdata2 = json.load(file, encoding='utf-8')

file=open('../json/message3.json', mode="r")
realbusdata3 = json.load(file, encoding='utf-8')
#!--------------------------------------

#!DUMMY DATA -----------------------------------
# file=open('Dummy/DummyStop_per_line.json', mode="r")
# stops_of_line = json.load(file, encoding='utf-8')

# file=open('Dummy/DummyLines_per_stop.json', mode="r")
# lines_of_stop = json.load(file, encoding='utf-8')

# file=open('Dummy/DummyStops.json', mode="r")
# stops = json.load(file, encoding='utf-8')

#!----------------------------------------------

def checkDirection(line,stops_array_t):
    """ 
    | This function returns the direction of the bus.
    | 0- means the bus is going to the end of the line
    | 1- means the bus is going to the start of the line
    | 2- means that the direction was not found
        
        
    .. note::
        * This is very primitive, can be improved.
        
    Args:
        line (int): detected line by the algorithm 
        stops_array_t (list): list of stops detected by the algorithm in the bus course
    
    :return: direction of the bus 0/1/2
    :rtype: int
        
    """
    
    direction = 2 # not detected
    for paragem_temp in reversed(stops_array_t):
        paragem_temp=int(paragem_temp)
        
        if paragem_temp == ends_turns2[line][0]:
       
            return 0
        if paragem_temp == ends_turns2[line][1]:
           
            return 1
        if paragem_temp == ends_turns2[line][2]:
            
            return  0 # sus
    

    return direction

def getLinesOfStop(stop_id):  #*WORKING
    """
    | This function returns the lines associated to a stop in the lines_of_stop.json
    
    Args:
        stop_id (int): id of the stop
    
    :return: array of lines associated to the stop
    :rtype: list
        
    """
    if stop_id == 0:
        return [1,2,3,4,5,6,8,10,11,12,13]
    #for stop in lines_of_stop:
    #    if str(stop_id) == stop:
    #        return lines_of_stop[stop]['lines'] #!Index 1 is the name of the stop
    try:
        return lines_of_stop[str(stop_id)]['lines']
    except:
        return []   

def ParagemUnica(paragem): 
    """
    | This function detects if a stop has only one line associated with it.
    
    Args:
        paragem (int): id of the stop
        
    :return: True/False
    :rtype: bool
    
    """
    paragem= str(paragem) #* WORKING
    # for stop in lines_of_stop:
    #     if paragem == stop and len(lines_of_stop[stop]['lines']) == 1:
    #         return True
    # return False
   
    try:
        return len(lines_of_stop[paragem]['lines']) == 1 if paragem != "0" else False
    except:
        return False #! ?

def checkStop(coordenadas): # check if a stop is nearby
    """
        | This function checks if a stop is nearby
        
        Args:
            coordenadas (list): coordinates of the bus
            
        :return: A tuple with the id of the stop and the distance to it
        :rtype: tuple
        
        .. note::
            The distance to check is set to 0.075km (75m)
            This can be changed in 
            | ``y := dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.075)``
            Just change the 0.075 to the desired distance
            
    """
    # candidates=[]
    # for stop in stops: #* WORKING
    #     tuple = dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.075) # 0.2 km is the range to check
    #     if tuple[0] : 
    #         candidates.append((stop, tuple[1])) if stop not in candidates else candidates 
    #     #return min of a tuple in the second argument and default value if there is no tuple
    # paragem=min(candidates, key=lambda x: x[1])[0] if candidates else 0
    # print("paragem -- " ,stops[str(paragem)]['name'])
   
    # return  paragem #!ID 0 means no stop is nearby
   
    #print("paragem --", min( [ (stop,y) for stop in stops if (y := dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.075))], 
     #       default=[0] , 
      #      key=lambda x: x[1])[0] )
    return(min( [ (stop,y) for stop in stops if (y := dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.075))], 
            default=[0] , 
            key=lambda x: x[1])[0] )
   

def Analise_stop(bus_id,paragem): 
                     
    """
    
    | This function makes the intersection of the possible lines detected by the algorithm previosly
    | with the lines of the stop that the bus passed through.
    | It also updates the global dictionary with the newly calculated possible lines.
    
    .. note::
        * This uses the global dictionaty bus_list to get the stored lines previously detected

    Args:
        bus_id (int): id of the bus
        paragem (int): id of the stop
        
    """
    #!DISCLAIMER:
    #When i did this only I and God knew how it worked, now only God knows
    #print("paragem_analise",paragem)
    linesofstop = getLinesOfStop(paragem) # return the lines that pass through the stop
    #print(linesofstop)
    
    # for line in stops_of_line: 
    #     for linha_guardada in bus_list[bus_id]: 
    #         if line == linha_guardada : # ha aqui u problema com as linhas que nao existem no json 
    #             possible_lines.append(line)
    
    possible_lines = [line for line in linesofstop for linha_guardada in bus_list[bus_id] if line == linha_guardada]
    bus_list[bus_id] = possible_lines # guarda as linhas possiveis


def Find_line_of_bus(bus, bus_id): #*TODO Find line(s) of bus by ID
    
    """
    | This function finds the line(s) possible of a bus by its ID given different travelled positions.
    | It is a confidence system so that it always gives out a line (correct or not)
    | It updates the database the highest confidence line detected.
    
    .. note::
        * This is the heart of the line detection algorithm and it uses the global dictionary bus_list
        * It calls many other functions to do the job.

    Args:
        bus (dict): dictionary with the bus data
        bus_id (int): id of the stop
        
    """
    stops_array=[]
    confidence = {}
    paragem=0
    if bus_id not in bus_list.keys():
        bus_list[bus_id] = [1,2,3,4,5,6,8,10,11,12,13]
    #check if id in dictionary
    for time in bus[bus_id]['data']:
        currenttimestamp=time
        if(len(bus_list[bus_id])==0):
            bus_list[bus_id] = [1,2,3,4,5,6,8,10,11,12,13]
        if(len(bus_list[bus_id])==1):
            temp= [1,2,3,4,5,6,8,10,11,12,13]
        #for coord in bus[bus_id]['data'][time]: # para cada paragem que esta no historico da OBU
        coord =(bus[bus_id]['data'][time]['coords']['lat'], bus[bus_id]['data'][time]['coords']['long'])
        possible_lines={}
        
        realparagem = checkStop(coord)
        paragem = realparagem if realparagem != 0 else paragem  # verificar se a paragem existe e devolve o ID dela 
       
        stops_array.append(paragem)
        # print(ParagemUnica(paragem))
        # print("checkstop",checkStop(coord))
        # print("paragem",paragem)
        if ParagemUnica(realparagem):
            bus_list[bus_id] = getLinesOfStop(paragem) # receber a linha da paragem (vai se so uma)
            if bus_id not in confidence.keys():
                confidence[bus_id] = {}
            if bus_list[bus_id][0] not in confidence[bus_id].keys():
                confidence[bus_id][bus_list[bus_id][0]] = {}
                confidence[bus_id][bus_list[bus_id][0]]['value'] = 0
                confidence[bus_id][bus_list[bus_id][0]]['stop'] = 0
            
            

            #! LINE 5 IS DIFFERENT IS NOT WORKING WITH CONFIDENCE
            confidence[bus_id][bus_list[bus_id][0]]['value'] = confidence[bus_id][bus_list[bus_id][0]]['value'] + 1 if paragem!= confidence[bus_id][bus_list[bus_id][0]]['stop'] else confidence[bus_id][bus_list[bus_id][0]]['value']
            confidence[bus_id][bus_list[bus_id][0]]['stop'] = paragem
            #return
        else:

            Analise_stop(bus_id,paragem) # compar com as linas possiveis obtidas anteriormente 
            
            if realparagem != 0:# com as linhas possiveis novas                                                                
                for i in range(len(bus_list[bus_id])):

                    if bus_id not in confidence.keys():
                        confidence[bus_id] = {}
                    if bus_list[bus_id][i] not in confidence[bus_id].keys():
                        confidence[bus_id][bus_list[bus_id][i]] = {}
                        confidence[bus_id][bus_list[bus_id][i]]['value'] = 0
                        confidence[bus_id][bus_list[bus_id][i]]['stop'] = 0
                    
                    #! LINE 5 IS DIFFERENT IS NOT WORKING WITH CONFIDENCE
                    confidence[bus_id][bus_list[bus_id][i]]['value'] = confidence[bus_id][bus_list[bus_id][i]]['value'] + 1 if paragem != confidence[bus_id][bus_list[bus_id][i]]['stop'] else confidence[bus_id][bus_list[bus_id][i]]['value']
                    confidence[bus_id][bus_list[bus_id][i]]['stop'] = paragem
                
                #print("linha unica",bus_list[bus_id])
            
    #print(max(confidence[bus_id],key=confidence[bus_id].get))
    try:
        aux = confidence[bus_id]
    except:
        return
    lineAndStop = max(aux.items(), key=lambda x: x[1]['value']) if aux else {}
    attribuited_line=(lineAndStop[0])
    last_stop = lineAndStop[1]['stop']
    
    
    
    direction = checkDirection(attribuited_line,stops_array)
    print(currenttimestamp)
    prediction = ETAmapbox.gps(str(attribuited_line), int(last_stop), int(direction), currenttimestamp)
  
    print("-----------------------------------------------------------------------------")
    print("bus_list:",bus_list)
    print(len(bus_list[bus_id]))
    print("paragem:",paragem)
    print("line:",bus_list[bus_id][0])
    print("bus_id: ",bus_id)
    print("CONFIDENCE :",confidence)
    print("attrLine",attribuited_line)
    print("LStop",last_stop)
    print("DIRECTION",direction)
    print("PREDICTION",prediction)
    print("-------------------------------------------")
    print()
    pymongo_functions.SendBusData(bus_id,list(bus[bus_id]['data'].keys())[-1],date.today().strftime("%d/%m/%Y"),attribuited_line,last_stop,prediction)
    pymongo_functions.MapBoxTimeStampsPrediction(attribuited_line,bus_id,last_stop,prediction)
    pymongo_functions.LinesData( attribuited_line,bus_id,last_stop)
    print("passou")
    
    


def filterData(bus,bus_id):
    
    """
    | This function filters the received data from the OBU history through Orion? and returns a dictionary with the filtered data.

    Args:
        bus (dict): dictionary with the bus data
        bus_id (int): id of the stop
        
    :return: Dictionary with the filtered data
    :rtype: dict
    """
    
    temp = {}
    temp[bus_id] = {}
    temp[bus_id]['data'] = {}
    temp2={}
    temp2[bus_id] = {}
    temp2[bus_id]['data'] = {}

    for time in reversed(bus['data'].keys()): 
        
        #time=bus[bus_id]['data'][item]
        coord =(bus['data'][time]['coords']['lat'], bus['data'][time]['coords']['long'])
        paragem = checkStop(coord) # verificar se a paragem existe e devolve o ID dela 
        
        temp[bus_id]['data'][time] = bus['data'][time]
        
        if int(paragem) in line_ends:
            temp2[bus_id]['data']={key:value for key,value in reversed(temp[bus_id]['data'].items())}
           
            return temp2
    
    return {bus_id:bus}       
    
    
def Line_detection(buses={}):
    """
    | Main function of the program. It receives the data from the OBU history and filters it through the filterData function.

    """
    #buses=realbusdata #! TESTES SEM SERVER
    print("---------------------")
    print(buses)
    print("----------yes-----------")
    
    for bus in buses:   
        bus_filter = filterData(buses[bus],bus)   
       
        Find_line_of_bus(bus_filter,bus) # descobrir se possível a linha do autocarro e avisar a aplicação mobile
        
#Line_detection(None) #!ISTO E PARA TESTES SEM SERVER


#----------------------------------------------------------------------------------------------------------
# python 3.6




#! ------------------------- ORION HISTORY -------------------------

# * credentials for the API
user_and_password = '{"username": "peci_2122_atcll","password": "pecII_2122_atcll+"}'
headers = {"Content-type": "application/json", "Accept-Charset": "UTF-8"}

# * array to select the services and types
services = ["aveiro_cam", "aveiro_radar", "transdev"]
types = ["Traffic", "Count", "Values"]

# * Create ORION Auth Token
def get_api_authtoken():
    """
    .. warning:: 
    
        | The credentials used for this code are private.
        | In order for this code to function, the credentials used must have authorization to subscribe to the CORE_SERVICES.
        | You must use your own credentials to run this code. The credentials can be replaced in the code below.
    
    .. code-block:: python

        user_and_password = '{"username": "[IT username here]","password": "[IT password here]"}'

    For this code there were also dictionaries with the headers in order to retrieve the Token from the API, and the services and types of data to subscribe.

    .. code-block:: python

            # Headers necessary for the API
            headers = {"Content-type": "application/json", "Accept-Charset": "UTF-8"}

            # array to select the services and types
            services = ["aveiro_cam", "aveiro_radar", "transdev"]
            types = ["Traffic", "Count", "Values"]

    
        
    * The Orion broker is located at 'https://orion.atcll-data.nap.av.it.pt'_.
    * The POST endpoint to obtain a token is located at '/auth', and requires the username and password as      the body of the request. 
    
    :return: If the user is authenticated correctly, the response headers will contain the ‘Authorization’ entry with a token in the format ‘Bearer {jwt}’.
    
    .. note:: The token will only be valid for one day.
    
    """
    
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
    """
    
    Makes the URL to get the historical data from the API.
    
    :param start_time, end_time make_history_url: Datetime date in milliseconds. 
    
    URL format::

    	https://api.atcll-data.nap.av.it.pt/history?type=obugps&start=str(start_time)&end=str(end_time) &attribute=location
    	
    * In this case, only the location attribute was inserted.
    
    """
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
    """
    Makes the historical request to the API.
    
    :param token first_arg: Authentication token obtained in get_api_authtoken function.
    :param url second_arg: URL obtained in make_history_url function.
    :param service third_arg: Service where you want to get the data.
    
    :return: Returns, in a json format, the service, data type and OBU of the bus.
    """
    r = requests.get(url, headers={"FIWARE-Service": service, "authorization": token})

    try:
        if r.json():
            print("HISTORY REQUEST SUCESSEFULL")
            return r.json()
        else:
            print("NO HISTORY DATA")
            return {}

    except:
        print(r.text)
        return {}


# * Converts a datetime date to milliseconds
def date_to_millisecconds(date):
    """
    Converts a datetime date to miliseconds.
    
    :param date date_to_milisecconds:  the datetime date has the format yyyy-mm-dd hh:mm:ss
    
    """
    return int(time.mktime(date.timetuple()) * 1000)


# * Get all the keys of the dictionary
# * retuns the list of keys sorted
def get_key_Values(dictionary):
    """
    Get all the keys of the dictionary
    
    :param dictionary get_key_Values: values in key:values pairs
    
    :return: List of keys sorted
    """
    keylist = list(dictionary.keys())
    keylist.sort()
    return keylist


# * Fix the time in the json from GMT to local time
def json_fix_time(json):
    """This function fixes the time in the json from GMT to local time
    This json is the one that is received from the function :func:`get_history_request`
    
    :param json json: Entire json with the historical data
    
    .. note::
        This function was used and created in mind with Daylight Saving Time.
        It was not tested with the standard time during winter.
        
    This function replaces the time for each bus with the time in local time.
    Each bus is a dictionary with the key ``["time"]`` and the value is a string with the time in GMT.
    
    .. code-block:: python

        # bus= "urn:ngsi-ld:obuGPS:transdev:50" where 50 is the bus number
        # GMTtime = "2022-03-30T08:25:51"
        
    And for each timestamp in the json, it is converted to local time.
    """
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
def make_IA_request():
    """This function return the formatted json for the Line Detection algorithm

    The function starts by getting the historical data from the API, which is done by setting the start and end time of the request.
    In this case, the start time is the current time minus one hour and the end time is the current time.
    
    .. code-block:: python

        dEnd = datetime.datetime.now()
        dStart = dEnd - datetime.timedelta(minutes=60)

    Then both the times are converted from datetime to milliseconds and the request is made to the API, using the url created by the function :func:`make_history_url`.
    
    If the request is successful, the function :func:`json_fix_time` is called to fix the time in the json, and is formatted to be used by the Line Detection algorithm with the function :func:`format_json`.
    
    
    :return: Json with the historical data correctly formatted
    :rtype: json
    """
    # * get the token
    token = get_api_authtoken()

    # * get the start and end time
    # * when this function is called, the end time is the current time
    #dStart = datetime.datetime(2022, 5, 9, 18, 0)
    #dEnd = datetime.datetime(2022, 5, 9, 19, 0)
    
    dEnd = datetime.datetime.now() 
    dStart = dEnd - datetime.timedelta(minutes=60)

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
        cleanJSON = format_json(requestJSON)
        return cleanJSON


# * Function to format the json for the AI request
def format_json(jsonn):
    """
    This function formats the json for the Line Detection algorithm.
    
    :param json jsonn: json with the historical data
    
    A new json is created with the following structure:
    
    .. code-block:: python
    
        {
            busID:{ #busID is the bus number (Example: "50")
                "data":{
                    datetime:{ #datetime is the datetime of the data (Example: "08:25:51")
                        "coords":{
                        "lat":40.6408937,
                        "long":-8.64804955
                        }
                    }
                }
            }
        }
    
    This new json is later returned by the function.
    
    :return: json with the data for the Line Detection algorithm
    :rtype: json
    """
    formatedJSON = {}
    # * gets all buses in the json
    for fullBusID in get_key_Values(jsonn):
        # * fullBusID = urn:ngsi-ld:obuGPS:transdev:50 where 50 is the bus number
        splitBusID = fullBusID.split(":")
        busID = int(splitBusID[4])
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
    """This function is called when the client wants to connect to the MQTT brokersubscribes to the MQTT_TOPIC set in a variable.
    The parameters are default from the the libray ``paho-mqtt``.
    
    """
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
    


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    """This function loads the message recieved from the MQTT broker
    
    It sends an IA request when the bus enters the range of the lamp-post.

    The function uses a global dictionary to store the busses that have past by a lamp-post.
    The busses are stored in the dictionary with the bus number as the key and the time of the last message as the value.
    For each bus, the dictionary is checked if the bus has passed by a lamp-post.
    If the bus has passed by a lamp-post, we check if the lamp-post is in bus keys.
        If the lamp-post is in the bus keys, we check if the bus is still passing by that dictionary and update the timestamp value in the dictionary
    Else, we add the bus to the dictionary with the current time as the value. and make an IA request.
    If the IA request is sucessful, we call the function :func:`Line_detection` to get the line detection data.
    """
    j_son = json.loads(msg.payload)
    if j_son["stationType"]==6: # Station Type (6) means it's a bus
        if j_son["stationID"] in y.keys(): #if it's in the dictionary, it means it already past by a lamp-post
            if j_son["receiverID"] in y[j_son["stationID"]].keys(): #if the bus already past by the lamp-post that is sending the message
            #Compare the timestamp of the bus in the dictionary and the current timestamp detected by the lamp-post
                if j_son["timestamp"] > y[j_son["stationID"]][j_son["receiverID"]]: # if the current timestamp is bigger than the dictionay timestamp, that means the bus is still moving in range of the lamp-post
                    y[j_son["stationID"]][j_son["receiverID"]] = j_son["timestamp"] # update the timestamp in the dictionary
                
            else: #first time the bus is passing by that lamp-post
                IAjson=make_IA_request()
                #print("IAjson: ",IAjson)
                if IAjson != {}:
                  Line_detection(IAjson)
                  y[j_son["stationID"]][j_son["receiverID"]] = j_son["timestamp"]
        else: # first time that bus is detected by any lamp-post
            IAjson=make_IA_request()
            if IAjson != {}:
                Line_detection(IAjson)
                y[j_son["stationID"]] = {}
                y[j_son["stationID"]][j_son["receiverID"]] = j_son["timestamp"]
                #print(y)
    
    #cleans the dictionay of the busses that have passed by a lamp-post and that are older than 1 minute
    y_copy = {**y}
    stationList = list(y.keys())
    for station in stationList:
        l = list(y_copy[station].keys())
        for receiverIDkey in l:
            if (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(y[station][receiverIDkey])).total_seconds()> 60:
                del y[station][receiverIDkey]
    

def connect_mqtt():
    """This is the function that connects to the MQTT broker.

    The function creates a new client and sets the callbacks for the :func:`on_connect` connection and the message.
    
    :return: The client connected to the broker
    :rtype: instance of ``mqtt.Client()``
    """
    # criar variavel para receber os dados
    receiver = mqtt.Client()
    receiver.on_connect = on_connect
    receiver.on_message = on_message
    receiver.connect_async("atcll-data.nap.av.it.pt", 1884, 60)
    
    return receiver


#! ------------------------- MAIN -------------------------

if __name__ == '__main__':
    try:
        print("entrou")
        receiver = connect_mqtt()
        print("2")
        receiver.loop_forever()
        print("3")
    except KeyboardInterrupt:
        print("\r  ")
        print("Exiting Program...")



# #----------------------------------------------------------------------------------------------------------

# #if __name__ == "__Line_detection__":
# #Line_detection()

# #Find_line_of_bus(bus,50)
# #print(bus_list)

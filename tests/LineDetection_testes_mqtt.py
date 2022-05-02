import json
import time
import distance as dist

import paho.mqtt.client as mqtt

bus_list = {}

global received_data
received_data=[] # receber data por mqtt

#!REAL DATA---------------------

file=open('json/stops per line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')

file=open('json/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')

file=open('json/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')
#!--------------------------------------

#!DUMMY DATA -----------------------------------
# file=open('Dummy/DummyStop_per_line.json', mode="r")
# stops_of_line = json.load(file, encoding='utf-8')

# file=open('Dummy/DummyLines_per_stop.json', mode="r")
# lines_of_stop = json.load(file, encoding='utf-8')

# file=open('Dummy/DummyStops.json', mode="r")
# stops = json.load(file, encoding='utf-8')

#!----------------------------------------------


def getLinesOfStop(stop_id):  #*WORKING Return the lines associated with a stop
    for stop in lines_of_stop:
        if str(stop_id) == stop:
            return lines_of_stop[stop]['lines'] #!Index 1 is the name of the stop
        

def ParagemUnica(paragem): #* WORKING Give stop and return if its the only stop in its line
    paragem= str(paragem) 
    for stop in lines_of_stop:
        if paragem == stop and len(lines_of_stop[stop]['lines']) == 1:
            return True
    return False

def checkStop(coordenadas): #* Working Receive Coordinates and return the nearest BusStop
    candidates=[]
    for stop in stops: #* WORKING
        tuple = dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.05) # 0.05 km is the range to check
        if tuple[0] : 
            candidates.append((stop, tuple[1])) if stop not in candidates else candidates 
    return min(candidates, key=lambda x: x[1])[0] if candidates else 0 #!ID 0 means no stop is nearby
   

def Analise_stop(bus_id,paragem): # from the id of the bus and the stop number, change the saved lines of 
                                # that bus so that it coincides with the lines of the stop that that bus passed through 
                                # ex : saved : [1,2,3,4]
                                # new : [4,5]
                                # change to : [4]
                                
    #!DISCLAIMER:
    #When i did this only I and God knew how it worked, now only God knows
    
    stops_of_line = getLinesOfStop(paragem) # return the lines that pass through the stop
    possible_lines = [] # array responsible for savong the possible lines
    
    for line in stops_of_line: 
        for linha_guardada in bus_list[bus_id]: 
            if line == linha_guardada : 
                possible_lines.append(line)
                
    bus_list[bus_id] = possible_lines # save the possible lines in the global dictionary
    return
    
def Find_line_of_bus(bus, bus_id): #*TODO Find line(s) of bus by ID
    
    if bus_list[bus_id] == None: # Initialize in case of new bus or Error
        bus_list[bus_id] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        
    #check if id in dictionary
    for time in bus['data']:
        for coord in bus['data'][time]: #For each coordinate received

            coord =(bus['data'][time]['coords']['lat'], bus['data'][time]['coords']['long'])
       
            paragem = checkStop(coord) #Check if the given coordinates are near a BusStop and get its ID
            print("hello")
            if paragem == 0:      
                continue
            else:
                if ParagemUnica(paragem): # Check if it only passed a line through this Stop
                    bus_list[bus_id] = getLinesOfStop(paragem) # If its a UniqueStop return the line of the stop
                    print("Linha %d atribuida ao autocarro %d" % (bus_list[bus_id][0], bus_id) ) # testing
                    return
                else:

                    Analise_stop(bus_id,paragem) # Compare the Stored possible lines with the new possible lines
                    
                    if(len(bus_list[bus_id])==1):
                        print("linha unica")
                    #     #TODO send linha á app

    if(len(bus_list[bus_id])==1):
        print("Linha %d atribuida ao autocarro %d" % bus_list[bus_id][0], int(bus_id) )
    #     #TODO send linha á app






def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("PECI_2122/BusData/Response")


def publish(sender,flag,bus_list=None):

    if flag:
        msg = json.dumps("Send_data")

        topic = "PECI_2122/BusData/Request"
        result = sender.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
    else:
        msg = json.dumps(bus_list)

        topic = "PECI_2122/BusData/BusLine"
        result = sender.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("teste")
    j_son = json.loads(msg.payload)
    global received_data
    received_data = j_son.items()
    print("Onmessage",received_data)

def connect_mqtt():
    # criar variavel para receber os dados
    receiver = mqtt.Client()
    receiver.on_connect = on_connect
    receiver.on_message = on_message
    receiver.connect_async("atcll-data.nap.av.it.pt", 1884, 60)

    return receiver

def Line_detection():
    receiver = connect_mqtt() # Connect mqtt
    time.sleep(3)
    while True:
        receiver.loop_start()

        publish(receiver,True) # receive data from mqtt server
        time.sleep(3)
        
        global received_data
        print("Received_data_dps:",received_data)
        for autocarro in received_data: # Process each received bus
            print("Autocarro:",autocarro)
            Find_line_of_bus(autocarro) # Run Algorithm for each bus

        
        publish(receiver,False,bus_list) # send data to mqtt server

        time.sleep(10)

Line_detection()

#Find_line_of_bus(bus,50)
#print(bus_list)

#coords=(40.64045,-8.651793333)
#print(checkStop(coords))

# bus={
#     "data":{
#         "11:14:13":{
#             "coords":{
#             "lat":40.640018333,
#             "long":-8.651246667
#             }
#         },
#         "11:14:22":{
#             "coords":{
#             "lat":40.64045,
#             "long":-8.651793333
#             }
#         },
#         "11:14:31":{
#             "coords":{
#                 "lat":40.640011,
#                 "long":-8.6406062
#             }
#         }
#     }   
# }

# print(getLinesOfStop(1364747314))
# print(ParagemUnica(1364747314)) #false
# print(ParagemUnica(5407623407)) #true

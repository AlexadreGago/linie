import json
import time
import distance as dist
from tests import pymongo_functions
import paho.mqtt.client as mqtt
from datetime import datetime
from datetime import date
import ETAmapbox
from tests import pymongo_functions

#!IMPORTS SILVEIRA

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

bus_list = {}

ends_turns= {1: (4873436913, 1364747314, 4873436913), #1
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

file=open('json/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')

file=open('json/message_trim.json', mode="r")
realbusdata = json.load(file, encoding='utf-8')

def checkStop(coordenadas): # check if a stop is nearby
    candidates=[]
    for stop in stops: #* WORKING
        tuple = dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.075) # 0.2 km is the range to check
        if tuple[0] : 
            candidates.append((stop, tuple[1])) if stop not in candidates else candidates 
        #return min of a tuple in the second argument and default value if there is no tuple
    paragem=min(candidates, key=lambda x: x[1])[0] if candidates else 0
    return  paragem #!ID 0 means no stop is nearby

bus_id='99'
def filterData(bus):
    temp = {}
    for time in reversed(bus[bus_id]['data'].keys()): 
        #time=bus[bus_id]['data'][item]
        coord =(bus[bus_id]['data'][time]['coords']['lat'], bus[bus_id]['data'][time]['coords']['long'])
        paragem = checkStop(coord) # verificar se a paragem existe e devolve o ID dela 
        print("paragem",paragem)
        print(line_ends)
        
        if int(paragem) in line_ends:
            return temp       
        temp[time] = bus[bus_id]['data'][time]
    return temp       


def Line_detection(bus):
    print()
    print("realbusdata",realbusdata)
    print()
    bus=realbusdata #!REAL SHIT
    bus_filter = filterData(bus)
    pprint.pprint(bus_filter)
Line_detection(None) #!>TIRAR QUANDO FOR PARA METER O SILVEIRA
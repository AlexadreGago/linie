import pymongo_functions

from datetime import date
import random
import time
from datetime import datetime

import json
import requests

date=date.today().strftime("%d/%m/%Y")

for i in range(100):
    print("Sending bus data... ",i)
    bus_id=str(i)
    timestamp=str(datetime.now().strftime('%H:%M:%S'))
    attribuited_line = random.randrange(1,13)
    last_stop = str(i) + str(i) + str(i)
    prediction = {'4852045630': '14:45:34', '5407993801': '15:20:44', '1699881440': '14:50:31', '5368271761': '14:51:34', '5368271758': '14:52:34', '1799473677': '15:08:43', '4852045623': '15:00:43', '4852088188': '15:01:30', '1699701236': '15:04:23', '4852045622': '15:05:27', '2808808538': '15:14:46', '1699892416': '15:16:12', '5368271760': '15:17:08', '5368271755': '15:18:06', '1699814700': '15:21:21', '4852088191': '15:21:53', '4852045631': '15:22:42', '1799461738': '15:25:55'}
    


    pymongo_functions.SendBusData(bus_id,timestamp,date,attribuited_line,last_stop,prediction)
    #pymongo_functions.MapBoxTimeStampsPrediction(attribuited_line,bus_id,last_stop,prediction)
    pymongo_functions.LinesData( attribuited_line,bus_id,last_stop)
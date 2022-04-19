import time
import json
import datetime
import requests
import pprint
from dateutil import tz

import paho.mqtt.client as mqtt


# Set the parameters of MQTT Broker connection 
BROKER = "atcll-data.nap.av.it.pt"
PORT = 1884
MQTT_TOPIC = [("PECI/BusData/Request",1)]
keepAlive = 60      ## default - Connection maintenance time in seconds

MQTT_TOPIC = [("PECI_2122/BusData/Request",1)]


#** This function will be called after connecting the client, and we can determine
#**  whether the client is connected successfully according to rc.
#* This function perfoms the subscription.
#! Note: Subscribing in on_connect() means that if we lose the connection and
#!        reconnect then subscriptions will be renewed.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

#* This function puts the AI request response under a certain topic
def publish(sender):
    msg =  json.dumps(make_IA_request())
    print("msg:",msg)
    topic = "PECI_2122/BusData/Response"
    result = sender.publish(topic, msg)
    print("Result",result)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

#* The on_message function gets the message when it comes in, as 
#*   well as the topic it was published under on
def on_message(client, userdata, msg):
    message = json.loads(msg.payload)
    global receiver
    if message == "Send_data":
        publish(receiver)
    else:
        y=False

#* Set Connecting Client ID
def connect_mqtt():
    receiver = mqtt.Client() #* Generating a random id for receiving data
    receiver.on_connect = on_connect
    receiver.on_message = on_message
    receiver.connect_async(BROKER, PORT, keepAlive)
    
    return receiver


global receiver
receiver = connect_mqtt()



#* credentials for the API
user_and_password='{"username": "peci_2122_atcll","password": "pecII_2122_atcll+"}'
headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

#* array to select the services and types
services = ['aveiro_cam','aveiro_radar','transdev']
types=['Traffic','Count','Values']

#* Create ORION Auth Token
def get_api_authtoken():
    res = requests.post("https://api.atcll-data.nap.av.it.pt/auth", data=user_and_password, headers=headers)    
    if res.status_code == 200:
        return res.headers.get('authorization')    
    
    print("Token is missing!!")
    print(res.text)

#* Makes the URL to get the data from the API
#* Receives the start and end time in milliseconds
def make_get_url(start_time,end_time):
    return 'https://api.atcll-data.nap.av.it.pt/history?type=obugps&start='+str(start_time)+'&end='+str(end_time)+'&attribute=location'

#* Makes the request to the API
#* Receives the token and the url and the service to subscribe
def get_request(token,url,service):
    r = requests.get(url, headers={
                        "FIWARE-Service": service,
                        "authorization": token
                    }) 
    
    try:
        if(r.json()):  
            print("REQUEST SUCESSEFULL")
            return r.json()
        else:
            print("NO DATA")
            return {}
            
    except:
        print(r.text)
        return {}

#* Converts a datetime date to milliseconds
def date_to_millisecconds(date):
    return int(time.mktime(date.timetuple())*1000)

#* Get all the keys of the dictionary
#* retuns the list of keys sorted
def get_key_Values(dictionary):
    keylist = list(dictionary.keys())
    keylist.sort()
    return keylist 

#* Fix the time in the json from GMT to local time
def json_fix_time(json):
    from_zone = tz.gettz('GMT')
    to_zone = tz.gettz('Europe/London')
    #*gets all buses in the json
    #* bus=  urn:ngsi-ld:obuGPS:transdev:50 where 50 is the bus number
    for bus in get_key_Values(json):
        i=0
        for GMTtime in json[bus]['time_index']:
            #* GMTtime = 2022-03-30T08:25:51
            tmp = GMTtime.split("T")
            
            tmpDate= tmp[0]
            tmpTime=tmp[1]
            
            splitDate = tmpDate.split("-")
            splitTime= tmpTime.split(":")
            
            #* puts the time_index date to datetime format
            datetimeGMT = datetime.datetime(int(splitDate[0]), int(splitDate[1]), int(splitDate[2]), int(splitTime[0]), int(splitTime[1]), int(splitTime[2]), 0)
            
            #* change the timezone
            datetimeGMT = datetimeGMT.replace(tzinfo=from_zone)
            datetimeLocal = datetimeGMT.astimezone(to_zone)
            
            #* puts the new time in the correct format
            newTime=str(datetimeLocal.year)+"-"+"{:02d}".format(datetimeLocal.month)+"-"+"{:02d}".format(datetimeLocal.day)+"T"+"{:02d}".format(datetimeLocal.hour)+":"+"{:02d}".format(datetimeLocal.minute)+":"+"{:02d}".format(datetimeLocal.second)

            #* replaces the old time with the new one
            json[bus]['time_index'][i]=newTime
            i+=1

#* function to handle the AI request
def make_IA_request():
    #* get the token
    token = get_api_authtoken() 
    
    #* get the start and end time
    #* when this function is called, the end time is the current time
    dEnd =  datetime.datetime.now() 
    dStart = dEnd - datetime.timedelta(minutes=60)
    
    #* convert the start and end time to milliseconds
    start_time = date_to_millisecconds(dStart)
    end_time = date_to_millisecconds(dEnd)
    
    #* make the url to get the data from the API
    url = make_get_url(start_time,end_time)
    
    #* make the request to the API
    requestJSON = get_request(token,url,services[2])
    
    #* if the json is empty that means no data was found for the time period
    #* puts in mqtt an empty array
    if requestJSON == {}:
        return {}
    #* if the json is not empty, fix the time and put the json in mqtt
    else:
        json_fix_time(requestJSON)
        cleanJSON=format_json(requestJSON)
        return cleanJSON

#* Function to format the json for the AI request
def format_json(json):
    formatedJSON = {}
    #* gets all buses in the json
    for fullBusID in get_key_Values(json):
        #* fullBusID = urn:ngsi-ld:obuGPS:transdev:50 where 50 is the bus number
        splitBusID = fullBusID.split(":")
        busID = int(splitBusID[4])
        
        formatedJSON[busID]={}
        formatedJSON[busID]["data"]={}
        
        #* puts in the formatedJSON the data for the bus by its time index
        for value in range(len((json[fullBusID]["time_index"]))):
            formatedJSON[busID]["data"][json[fullBusID]["time_index"][value].split("T")[1]]={"coords": {"lat": json[fullBusID]["lat"][value], "long": json[fullBusID]["long"][value]}}
    return formatedJSON


if __name__ == '__main__':
    try:
        
        while True:
            receiver.loop_start()
    except KeyboardInterrupt:
        print("\r  ")
        print("Exiting Program...")
    
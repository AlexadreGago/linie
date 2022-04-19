import time
import json

import paho.mqtt.client as mqtt



global y
y={}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
    # test
    #client.subscribe("+/jetson/radar/traffic/#")
    
    #bus info
    client.subscribe("+/apu/cam")
    
    # test obu it
    #client.subscribe("lab/cam")

def publish(sender):
    global y
    while True:
        time.sleep(1)
        if len(y)!=0:
            msg = json.dumps(y)
            
            topic = "PECI/BusData/ID"+str(y["stationID"])
            result = sender.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    j_son = json.loads(msg.payload)
    print(j_son)
    print()
    global y
    if j_son["stationType"]==6: # Station Type (6) significa que é um autocarro
        x = {
            "receiverID" : j_son["receiverID"], # ID da estaçao que está a receber os dados
            "stationID" : j_son["stationID"], # ID do bus
            "latitude" : j_son["latitude"],
            "longitude" : j_son["longitude"],
            "altitude" : j_son["altitude"],
            "speed" : j_son["speed"]
        }
        y = x
    else:
        y={}
    

def connect_mqtt():
    # criar variavel para receber os dados
    receiver = mqtt.Client()
    receiver.on_connect = on_connect
    receiver.on_message = on_message
    receiver.connect_async("atcll-data.nap.av.it.pt", 1884, 60)
    
    return receiver

def run():
    receiver = connect_mqtt()
    receiver.loop_start()
    publish(receiver)


if __name__ == '__main__':
    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("\r  ")
        print("Exiting Program...")

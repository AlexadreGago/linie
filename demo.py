import testsMain as ld
import pprint
import pymongo
import json

bus2={
    "data":{
        "11:14:13":{ # perto de baixo baixo
            "coords":{
            "lat":40.622980,
            "long": -8.651144
            }
        },
        "11:14:22":{ # perto de baixo
            "coords":{
            "lat":40.622658,
            "long": -8.651294
            }
        },
        "11:14:31":{# perto do centro
            "coords":{
                "lat":40.624531,
                "long": -8.649663
            }
        },
          "11:14:32":{ # Perto de nordeste
            "coords":{
                "lat": 40.624795, 
                "long": -8.647746
            }
        },
        "11:14:33":{ # londe de todas as paragens
            "coords":{
                "lat": 40.624075, 
                "long": -8.658793
            }
        }
    }   
}
bus3={
    "data":{
        "11:14:13":{ # perto de baixo baixo
            "coords":{
            "lat":40.622980,
            "long": -8.651144
            }
        },
        "11:14:22":{ # perto de baixo
            "coords":{
            "lat":40.622658,
            "long": -8.651294
            }
        },
                "11:14:33":{ # londe de todas as paragens
            "coords":{
                "lat": 40.624075, 
                "long": -8.658793
            }
        },
        "11:14:31":{# perto do centro
            "coords":{
                "lat":40.624531,
                "long": -8.649663
            }
        },
          "11:14:32":{ # Perto de nordeste
            "coords":{
                "lat": 40.626835,
                "long": -8.647732
            }
        }
    }   
}

bus4={
    "data":{
        "11:14:13":{ # perto de baixo baixo
            "coords":{
            "lat":40.622980,
            "long": -8.651144
            }
        },
        "11:14:22":{ # perto de baixo
            "coords":{
            "lat":40.622658,
            "long": -8.651294
            }
        },
                "11:14:33":{ # londe de todas as paragens
            "coords":{
                "lat": 40.624075, 
                "long": -8.658793
            }
        },
        "11:14:31":{# perto do centro
            "coords":{
                "lat":40.624531,
                "long": -8.649663
            }
        },
          "11:14:32":{ # Perto de este
            "coords":{
                "lat": 40.623105, 
                "long":-8.646884
            }
        }

    }   
}
bus5={
    "data":{
        "11:14:13":{ # perto de baixo baixo
            "coords":{
            "lat":40.622980,
            "long": -8.651144
            }
        },
        "11:14:22":{ # perto de baixo
            "coords":{
            "lat":40.622658,
            "long": -8.651294
            }
        },
                "11:14:33":{ # londe de todas as paragens
            "coords":{
                "lat": 40.624075, 
                "long": -8.658793
            }
        },
        "11:14:31":{# perto do centro
            "coords":{
                "lat":40.624531,
                "long": -8.649663
            }
        },
        


    }   
}


file=open('json/message.json', mode="r")
bus = json.load(file, encoding='utf-8')
# print(ld.ParagemUnica(7))
# print(ld.checkStop((40.624795, -8.647746)))
#ld.Find_line_of_bus(bus1, 1)

#pprint.pprint(bus2)
#print(ld.bus_list)

#measure execution time
import time
start_time = time.time()
#ld.Find_line_of_bus(bus2, 2)
stop_time = time.time()

#ld.Find_line_of_bus(bus3, 3)
#ld.Find_line_of_bus(bus4, 4)

x = ld.Find_line_of_bus(bus['99'], 52)
print(x)


#stop2_time = time.time()


# print("1 autocarro : " ,stop_time - start_time)
# print( "todos os autocarros : " ,stop2_time - start_time)

#------------------------------------------------------------
#Send data to database

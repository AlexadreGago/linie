import tests.tests_begining as ld
import pprint
import pymongo

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
# print(ld.ParagemUnica(7))
# print(ld.checkStop((40.624795, -8.647746)))
#ld.Find_line_of_bus(bus1, 1)

#pprint.pprint(bus2)
#print(ld.bus_list)

#measure execution time
import time
start_time = time.time()
ld.Find_line_of_bus(bus2, 2)
stop_time = time.time()

ld.Find_line_of_bus(bus3, 3)
ld.Find_line_of_bus(bus4, 4)
ld.Find_line_of_bus(bus5, 5)
stop2_time = time.time()


# print("1 autocarro : " ,stop_time - start_time)
# print( "todos os autocarros : " ,stop2_time - start_time)

#------------------------------------------------------------
#Send data to database
import time
import datetime

keys_values = ld.bus_list.items()

dic={}
dic["time"] = str(datetime.datetime.now().time())
dic["bus_list"] = {str(key): (value) for key, value in keys_values}

myclient = pymongo.MongoClient("mongodb://localhost:27017/") # connect to mongo db

db = myclient["database_lines"] # acess the database

day = db[str(datetime.date.today())]# get/create the collection

#x = day.insert_one(dic) # insert data

#--------------------------------------------------------------
#get day from database
days = db.list_collection_names()
print(days)

day = db[str(datetime.date.today())]

cursor = day.find({}) # cursor no incio do documento

data = list(cursor) # devolve lista da collection
temp=[]
for a in data: # iterar a collection para receber os tempos
    temp.append(a["time"])

myquery = {"time": min(temp)} # escolher o tempo desejado para receber

dia = day.find(myquery) # procurar na collection esse tempo

for x in dia:
    dados_fim = x
 
print(dados_fim)
print(dados_fim["bus_list"])
import json
import time
import distance as dist

import paho.mqtt.client as mqtt

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

# received_data=[] # receber data por mqtt

# file=open('json/stops per line.json', mode="r")
# stops_of_line = json.load(file, encoding='utf-8')

# file=open('json/lines of stop.json', mode="r")
# lines_of_stop = json.load(file, encoding='utf-8')

# file=open('json/stops.json', mode="r")
# stops = json.load(file, encoding='utf-8')
#!--------------------------------------

#!DUMMY DATA -----------------------------------
file=open('Dummy/DummyStop_per_line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')

file=open('Dummy/DummyLines_per_stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')

file=open('Dummy/DummyStops.json', mode="r")
stops = json.load(file, encoding='utf-8')

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
    return min(candidates, key=lambda x: x[1])[0] if candidates else 0 #!ID 0 means no stop is nearby
   

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
    return # atualizacao das linhas possiveis
    
def Find_line_of_bus(bus, bus_id): #*TODO Find line(s) of bus by ID
    
    #bus_id = 50
    if bus_id not in bus_list.keys():
        bus_list[bus_id] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    #check if id in dictionary
    for time in bus['data']:
        for coord in bus['data'][time]: # para cada paragem que esta no historico da OBU
            print(bus_list)
            coord =(bus['data'][time]['coords']['lat'], bus['data'][time]['coords']['long'])
       
            paragem = checkStop(coord) # verificar se a paragem existe e devolve o ID dela 
            if paragem == 0:   
               
                continue 
            else:
              
                if ParagemUnica(paragem):
                    bus_list[bus_id] = getLinesOfStop(paragem) # receber a linha da paragem (vai se so uma)
                   
                    return
                else:
                   
                    Analise_stop(bus_id,paragem) # compar com as linas possiveis obtidas anteriormente 
                                                                    # com as linhas possiveis novas
                    if(len(bus_list[bus_id])==1):
                        print("linha unica")
                    #     #TODO send linha á app

    #else: # autocarro novo

     #       for coordenada in received_data.autocarro.coordenadas: # para cada paragem que esta no historico da OBU
      #          paragem = checkStop(coordenada) # verificar se a paragem existe e devolve o ID dela 
       #         bus[id_bus] = getLinesOfStop(paragem) # receber a(s) linha(s) da paragem 



    if(len(bus_list[bus_id])==1):
        print("Linha %d atribuida ao autocarro %d" % bus_list[bus_id][0], int(bus_id) )
    #     #TODO send linha á app

    
# print(getLinesOfStop(1364747314))
# print(ParagemUnica(1364747314)) #false
# print(ParagemUnica(5407623407)) #true

#coords=(40.64045,-8.651793333)

#print(checkStop(coords))




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




def Line_detection():

    while True:

        for autocarro in received_data: # processar os dados autocarro a autocarro
            Find_line_of_bus(autocarro) # descobrir se possível a linha do autocarro e avisar a aplicação mobile


#if __name__ == "__Line_detection__":
#Line_detection()

#Find_line_of_bus(bus,50)
#print(bus_list)



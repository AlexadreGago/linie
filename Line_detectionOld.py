# Python dictionary is a built-in type that supports key-value pairs.
import json
import distance as dist
import time

import paho.mqtt.client as mqtt


autocarros ={}

received_data={} # receber data por mqtt

file=open('jsons/stops per line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')

file=open('jsons/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')

file=open('jsons/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')



def getLinesOfStop(stop_id):  #*WORKING
    for stop in lines_of_stop:
        if str(stop_id) == stop:
            return lines_of_stop[stop]['lines']
        
        
def Analise_stop(id_bus,paragem): # da-lhe o id do autocarro e a paragem a analisar e retorna as linhas possiveis
                                    #as linhas da paragem e as linhas guardadas anteriormente

    linhas_paragem = getLinesOfStop(paragem) # retornar as linhas possiveis para cada paragem
    linhas_temp = [] # array para guardar as linhas possiveis

    for linha in linhas_paragem: # DEIXAR SO AS PARAGENS IGUAIS
        for linha_existente in autocarros[id]:# linhsa guardadas no array autocarros
            if linha == linha_existente : # ha aqui u problema com as linhas que nao existem no json 
                linhas_temp += linha

    return linhas_temp # atualizacao das linhas possiveis


def checkStop(coordenadas): # verificar se a paragem existe
    candidates=[]
    for stop in stops: #* WORKING
        tuple = dist.check(coordenadas,(stops[stop]['lat'], stops[stop]['lon']), 0.2)
        if tuple[0] : 
            candidates.append((stop, tuple[1])) if stop not in candidates else candidates 
        #return min of a tuple in the second argument
    return min(candidates, key=lambda x: x[1])[0]


def ParagemUnica(paragem): # give stop and return if its the only stop in its line
    paragem= str(paragem) #* WORKING
    for stop in lines_of_stop:
        if paragem == stop and len(lines_of_stop[stop]['lines']) == 1:
            return True
    return False



def Find_line_of_bus(received_data,autocarro): #*TODO Find line(s) of bus by ID
    
    id_bus = autocarro.id

    #check if id in dictionary
    if id_bus in autocarros.keys():# ja apareceu
        for coordenada in received_data.autocarro.coordenadas: # para cada paragem que esta no historico da OBU
            paragem = checkStop(coordenada) # verificar se a paragem existe e devolve o ID dela 
            if ParagemUnica(paragem):
                autocarro[id_bus] = getLinesOfStop(paragem) # receber a linha da paragem (vai se so uma)
            else:
                autocarros[id_bus] = Analise_stop(id_bus,paragem) # compar com as linas possiveis obtidas anteriormente 
                                                                  # com as linhas possiveis novas


    else: # autocarro novo
        if received_data.autocarros.id not in autocarros:
            autocarros[id_bus] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            for coordenada in received_data.autocarro.coordenadas: # para cada paragem que esta no historico da OBU
                paragem = checkStop(coordenada) # verificar se a paragem existe e devolve o ID dela 
                autocarro[id_bus] = getLinesOfStop(paragem) # receber a(s) linha(s) da paragem 



    if(len(autocarros[id_bus])==1):
        print("linha %d atribuida ao autocarro ",autocarros[id_bus],id_bus)
        #TODO Update Database



    #se existir ver se ja tem linha atribuida senao remove linhas impossiveis
    #se nao existir é porque chegou á primeira paragem do dia e meter todas as linhas dessa paragens possiveis 
    # e ver historico da OBU a ver se se consegue atrivuir uma linha
    #tambem se pode ver a hora a que o autocarro chega e atribui-lhe uma linha (hardcoded)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("PECI_2122/BusData/Response")

def on_message(client, userdata, msg):
    j_son = json.loads(msg.payload)
    received_data = j_son

def connect_mqtt():
    # criar variavel para receber os dados
    receiver = mqtt.Client()
    receiver.on_connect = on_connect
    receiver.on_message = on_message
    receiver.connect_async("atcll-data.nap.av.it.pt", 1884, 60)
    
    return receiver

def publish(sender):
            
    topic = "PECI_2122/BusData/Request"
    msg = "Send_data"

    result = sender.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def Line_detection():
    while(True):

        receiver = connect_mqtt()
        receiver.loop_start()
        publish(receiver)

        #when a new bus appears in real-time
        #get history of the last hour 

        for autocarro in received_data[autocarro]: # processar os dados autocarro a autocarro
            Find_line_of_bus(autocarro) # descobrir se possível a linha do autocarro e avisar a aplicação mobile

        time.sleep(1)


if __name__ == "__Line_detection__":
    Line_detection()

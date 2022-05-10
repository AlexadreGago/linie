import requests
import json
import testsMain as testsMain
import urllib.parse
import datetime

def gps(line, current, sentido):
    file=open('json/stops per line.json', mode="r")
    stops_of_line = json.load(file, encoding='utf-8')

    file=open('json/lines of stop.json', mode="r")
    lines_of_stop = json.load(file, encoding='utf-8')

    file=open('json/stops.json', mode="r")
    stops = json.load(file, encoding='utf-8')

    file=open('json/stops of line lists.json', mode="r")
    stops_of_line_lists=json.load(file, encoding='utf-8')

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
                
    # line_ends= map (lambda x:(x[2]),ends_turns)


    # line='11'
    # current=4874315940
    # sentido=1
    str=""


    if sentido==2:
        return "Sentido errado"
    
    try:
        turn=stops_of_line_lists[line].index(ends_turns[int(line)][1])
    except:
        turn=0
    try:
        index=stops_of_line_lists[line].index(current, 0) if sentido==0 else stops_of_line_lists[line].index(current,turn)
    except:
        index=-1
    #end_index=stops_of_line_lists[line].index(ends_turns[int(line)][2])

    token = "pk.eyJ1IjoiaXRhdiIsImEiOiJjbDIwaWRwZ3Ywd3E3M2JscDB1ZjV0bzh2In0.JNCksFOjVnpes6dbdYR24w"

    count=0

    if index==-1:
        print("Não encontrado")
    else:
        
        for stop in stops_of_line[line][index:]:
            count+=1
            if count>25:
                break
            else:
                print(stop['lon'],"," ,stop['lat'], ";")
                str+="{},{};".format(stop['lon'],stop['lat'])

        print("-----------------------------------------------------")
        print(str)
        url="https://api.mapbox.com/directions/v5/mapbox/driving/{}?alternatives=false&continue_straight=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(str[:-1],token)
        print(url)
        response = requests.get(url)
        response=response.json()

        # with open('json/line1.json', 'w') as outfile:
        #     json.dump(response.json(), outfile, ensure_ascii=False)
        # print(response.json())

        now = datetime.datetime.now()
        index2=index
        for waypoint in response['routes'][0]['legs']: #paragens na linha, +1 porque range exclyui o ultimo valor
                index2+=1
                now+= datetime.timedelta(0, waypoint['duration'])
                print(stops_of_line_lists[line][index2],now.strftime("%H:%M:%S"))

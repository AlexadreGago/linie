import requests
import json
import urllib.parse
import datetime

def gps(line, current, sentido):
    """ 
        | This function returns the next 24 stops of the line and the time to arrive at each one
        | Depending on **sentido** it will search for **current** stop:
        * 0 : Search from the beginning until the turning point.
        * 1 : Search from the turning point until the end.
        | This needs to be done as the line can contain the same stop more than 1 time.
        | If **sentido** = 2 is given (direction not found) the function will count
        | the occurences of **current** in **line** because if **current** appears only once
        | it can still calculate the next 24 stops without "knowing" the direction.

    
    .. note::
        * 24 because 25 is the limit of waypoints by MapBox
        
    .. warning::
        * A strange prediction can be made in some cases as the stops dataset isn't complete
        * A strange response can occur if the 100.000 MapBox monthly requests are exceeded
        
    Args:
        line (int): Line number
        current (int): Current stop
        sentido (int): Direction of the line
    
    :return: Dictionary with the next 24 stops and the Estimated Time of Arrival
    :rtype: dict
        
    """
    file=open('../json/stops per line.json', mode="r")
    stops_of_line = json.load(file, encoding='utf-8')

    file=open('../json/lines of stop.json', mode="r")
    lines_of_stop = json.load(file, encoding='utf-8')

    file=open('../json/stops.json', mode="r")
    stops = json.load(file, encoding='utf-8')

    file=open('../json/stops of line lists.json', mode="r")
    stops_of_line_lists=json.load(file, encoding='utf-8')

    ends_turns= {1: (4873436913, 1364747314, 4873436913), #1
                2: (4873436915, 5403604506, 5398020251), #2
                3: (4873436913, 1364747314, 4873436913), #3
                4: (5401229911, 1364747314, 5401229910), #4
                5: (5398378854, 1364747314, 5398378854), #5
                6: (5395534183, 1364747314, 5395534182), #6
                8: (5410260321, 5398378854, 5410260321), #8
                10:(5410259987, 5398378854, 5410259986), #10
                11:(1699701236, 0000000000, 4852045631), #11 #!0 in turning pont means the line doesnt have a turning point it is circular
                12:(5410259987, 5405326919, 5410259986), #12
                13:(5407623407, 4852088188, 1799461738)} #13
                # Start     ,  Turn     ,   End
                
    # line_ends= map (lambda x:(x[2]),ends_turns)

    string=""
    print("count:", stops_of_line_lists[line].count(current))
    try:
        turn=stops_of_line_lists[line].index(ends_turns[int(line)][1])
        if sentido==2:

            if stops_of_line_lists[line].count(current) == 1: #if stop only appears once get index
                
                index=stops_of_line_lists[line].index(current) 
            else:
                return {}
                       
       # print("Turn: ",turn)
        else:
            if turn !=0 :
                index=stops_of_line_lists[line].index(current, 0, turn) if sentido==0 else stops_of_line_lists[line].index(current,turn)
            else:
                index=stops_of_line_lists[line].index(current)
    except:
        turn=0
        index=-1
    

    token = "pk.eyJ1IjoiaXRhdiIsImEiOiJjbDIwaWRwZ3Ywd3E3M2JscDB1ZjV0bzh2In0.JNCksFOjVnpes6dbdYR24w"

    count=0

    if index==-1:
        print("Stop not found")
        return {}
    else:        
        for stop in stops_of_line[line][index:]:
            count+=1
            if count>25:
                break #pardon the break
            else:
                #print(stop['lon'],"," ,stop['lat'], ";")
                string+="{},{};".format(stop['lon'],stop['lat'])

      
        url="https://api.mapbox.com/directions/v5/mapbox/driving/{}?alternatives=false&continue_straight=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(string[:-1],token)
     
        response = requests.get(url)
        response=response.json()

        # with open('json/line1.json', 'w') as outfile:
        #     json.dump(response.json(), outfile, ensure_ascii=False)
        # print(response.json())

        now = datetime.datetime.now()
        index2=index
        returns={}
        for waypoint in response['routes'][0]['legs']: #paragens na linha, +1 porque range exclyui o ultimo valor
                index2+=1
                now+= datetime.timedelta(0, waypoint['duration'])
                returns[str(stops_of_line_lists[line][index2])]=str(now.strftime("%H:%M:%S"))
                print(stops_of_line_lists[line][index2],now.strftime("%H:%M:%S"))
        return returns

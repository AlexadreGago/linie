 
#?This uses the stops per line json to get each stop and its name and coords

import json
file=open('../stops per line.json', mode="r")
lines_with_stops = json.load(file, encoding='utf-8')
line_id=0

# cleanjson={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[]}
stops = dict()


for line in lines_with_stops:
    for stop in lines_with_stops[line]:
        if stop['id'] not in stops:
            stops[stop['id']]={'name':stop['name'], 'lat' : stop['lat'], 'lon' : stop['lon']}

with open('../stops.json', 'w') as outfile:
    print(stops)
    json.dump(stops, outfile, ensure_ascii=False)


 
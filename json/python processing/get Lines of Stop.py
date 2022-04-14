

#?this uses stops per line json to get each stop and the lines that pass through it

import json
from pathlib import Path


file=open('../stops per line.json', mode="r")
lines_with_stops = json.load(file, encoding='utf-8')
line_id=0

# cleanjson={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[]}
linesofstop = dict()


for line in lines_with_stops:
    for stop in lines_with_stops[line]:
        for line2 in lines_with_stops:
            for stop2 in lines_with_stops[line2]:
                if stop2['id'] == stop['id']:
                    if stop['id'] not in linesofstop:
                        linesofstop[stop['id']]={'name':stop['name'], 'lines' : [] }
                    linesofstop[stop['id']]['lines'].append(int(line2)) if int(line2) not in linesofstop[stop['id']]['lines'] else linesofstop[stop['id']]['lines']
                    

with open('../lines of stop.json', 'w') as outfile:
     print(linesofstop)
     json.dump(linesofstop, outfile, ensure_ascii=False)



#?this gets the last stop of a line as well as the turning point

import json
from pathlib import Path


file=open('../stops per line.json', mode="r")
lines_with_stops = json.load(file, encoding='utf-8')
line_id=0

# cleanjson={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[]}
linesofstop = dict()
ends_turns=[(4873436913, 1364747314, 4873436913), #1
            (4873436915, 5403604506, 5398020251), #2
            (4873436913, 1364747314, 4873436913), #3
            (5401229911, 1364747314, 5401229910), #4
            (5398378854, 1364747314, 5398378854), #5
            (5395534183, 1364747314, 5395534182), #6
            (5410260321, 5398378854, 5410260321), #8
            (5410259987, 5398378854, 5410259986), #10
            (1699701236,),
            (5410259987, 5405326919, 5410259986), #12
            (5407623407, 4852088188, 1799461738)] #13
#for id 
#    for line in lines_with_stops:
    
        # for line2 in lines_with_stops:
        #     for stop2 in lines_with_stops[line2]:
        #         if stop2['id'] == stop['id']:
        #             if stop['id'] not in linesofstop:
        #                 linesofstop[stop['id']]={'name':stop['name'], 'lines' : [] }
        #             linesofstop[stop['id']]['lines'].append(int(line2)) if int(line2) not in linesofstop[stop['id']]['lines'] else linesofstop[stop['id']]['lines']
                    

with open('../lines of stop.json', 'w') as outfile:
     print(linesofstop)
     json.dump(linesofstop, outfile, ensure_ascii=False)



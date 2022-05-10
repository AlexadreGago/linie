import json
file=open('../stops per line.json', mode="r")
lines_with_stops = json.load(file, encoding='utf-8')

list={}
for line in lines_with_stops:
    list[line]=[]
    for stop in lines_with_stops[line]:
        list[line].append(stop['id'])


with open('../stops of line lists.json', 'w') as outfile:
     print(list)
     json.dump(list, outfile, ensure_ascii=False)



import json
import datetime
file=open('json/line13.json', mode="r")
linha13 = json.load(file, encoding='utf-8')
now = datetime.datetime.now()

file=open("json/stops per line.json", mode="r")
ids = json.load(file, encoding='utf-8')

for number in range(len(linha13['routes'][0]['legs'])): #paragens na linha, +1 porque range exclyui o ultimo valor
        now+= datetime.timedelta(0, linha13['routes'][0]['legs'][number]['duration'])
        print(ids['13'][number]['id'],now.strftime("%H:%M:%S"))

print("a")
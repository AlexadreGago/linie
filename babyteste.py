import json
import time
import distance as dist


file=open('json/stops per line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')

file=open('json/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')

file=open('json/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')

file=open('json/stops.json', mode="r")
ends_of_line = json.load(file, encoding='utf-8')

file=open('json/message.json', mode="r")
realbusdata = json.load(file, encoding='utf-8')


dic={}
dic['stops']=[1,2]
print(dic)
dic={}
print(dic)
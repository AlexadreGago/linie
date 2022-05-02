import requests
import json
import tests
import urllib.parse

file=open('json/stops per line.json', mode="r")
stops_of_line = json.load(file, encoding='utf-8')
file=open('json/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')
file=open('json/stops.json', mode="r")
stops = json.load(file, encoding='utf-8')

token = "pk.eyJ1IjoiaXRhdiIsImEiOiJjbDIwaWRwZ3Ywd3E3M2JscDB1ZjV0bzh2In0.JNCksFOjVnpes6dbdYR24w"

url = "https://api.mapbox.com/directions/v5/mapbox/driving/-8.6547145 , 40.6316261 ;-8.6557297 , 40.6349165 ;-8.6560068 , 40.640963?alternatives=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(token)


#print(url)
# count=0
#response = requests.get("https://api.mapbox.com/directions/v5/mapbox/driving/-8.6547145%2C40.6316261%3B-8.6557297%2C40.6349165?alternatives=false&geometries=geojson&overview=simplified&steps=false&access_token=pk.eyJ1IjoiaXRhdiIsImEiOiJjbDIwaWRwZ3Ywd3E3M2JscDB1ZjV0bzh2In0.JNCksFOjVnpes6dbdYR24w")

# print(response)
# for line in stops_of_line:
   
#     print(line, "line")
#     count = 0
str=""
#for line in stops_of_line:
for stop in stops_of_line['13']:
    print(stop['lon'],"," ,stop['lat'], ";")
    str+="{},{};".format(stop['lon'],stop['lat'])

url="https://api.mapbox.com/directions/v5/mapbox/driving/{}?alternatives=false&continue_straight=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(str[:-1],token)
print(url)
response = requests.get(url)

with open('json/line1.json', 'w') as outfile:
     json.dump(response.json(), outfile, ensure_ascii=False)
#print(response.json())
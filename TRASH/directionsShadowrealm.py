import requests
import json
import src.testsMain as testsMain
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

posicao="-8.5998204,40.6813118" #!vem da app


str1="{};".format(posicao)
str2=""
str3=""
final={}
line = '1' #vem da funcao que pede

length= len(stops_of_line[line])


for i in range(length) :
    
    stop = stops_of_line[line][i]
    if (i<=24):
        print(stop['lon'],"," ,stop['lat'], ";")
        str1+="{},{};".format(stop['lon'],stop['lat'])
        
    elif (i>24 and i<=49):
        print(stop['lon'],"," ,stop['lat'], ";")
        str2+="{},{};".format(stop['lon'],stop['lat'])
    else:
        print(stop['lon'],"," ,stop['lat'], ";")
        str3+="{},{};".format(stop['lon'],stop['lat'])
        

url1="https://api.mapbox.com/directions/v5/mapbox/driving/{}?alternatives=false&continue_straight=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(str1[:-1],token)
url2="https://api.mapbox.com/directions/v5/mapbox/driving/{}?alternatives=false&continue_straight=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(str2[:-1],token) if str2 else None
url3="https://api.mapbox.com/directions/v5/mapbox/driving/{}?alternatives=false&continue_straight=false&geometries=geojson&overview=simplified&steps=false&access_token={}".format(str3[:-1],token) if str3 else None

response = requests.get(url1).json()
response2= requests.get(url2).json() if url2 else {}
response3= requests.get(url3).json() if url3 else {}
print(url1)

for number in range(len(response['routes'][0]['legs'])):
    if (number<=24):
        final[number]=response['routes'][0]['legs'][number]['duration']
    elif (number>24 and number<=49):
        final[number]=response2['routes'][0]['legs'][number-25]['duration']
    else:
        final[number]=response3['routes'][0]['legs'][number-50]['duration']


with open('json/line1.json', 'w') as outfile:
     json.dump(final, outfile, ensure_ascii=False)
#print(response.json())
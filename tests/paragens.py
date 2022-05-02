import json
linha={}

#create dictionary with tag as number and name as text
def create_dict(file):
    with open(file) as f:
        data = json.load(f)
    d = {}
    for i in data:
        d[i["tag"]] = i["name"]
    return d

file=open('json.json')
stops=json.load(file)
import json, urllib.request
api_urls = ["http://data.hisparc.nl/api/"]
def getData(url,jsonCat = None):
    url = urllib.request.urlopen(url)
    data = json.loads(url.read().decode())
    if jsonCat == None:
        return data
    #elif type(jsonCat) == "str":
    try:
        str(jsonCat)
        return data[jsonCat]
    except TypeError:
        pass
    #elif type(jsonCat) == "list":
    try:
        list(jsonCat)
        while len(jsonCat) != 0:
            data = data[jsonCat[0]]
            jsonCat.pop(0)
        return data
    except TypeError:
        pass
print("MAIN API REQUESTS")
#with urllib.request.urlopen(api_url) as url:
    #data = json.loads(url.read().decode())
print(getData(api_urls[0]))
    #print(data["clusters"])
print(getData(api_urls[0],jsonCat="clusters"))

api_urls.append(api_urls[0]+getData(api_urls[0],jsonCat="clusters"))

print(getData(api_urls[1]))

cluster_json = getData(api_urls[1])

print("CLUSTERS")
for cluster in cluster_json:
    print(cluster["name"]+" "+str(cluster["number"]))

name = input("Cluster name? ")

for cluster in cluster_json:
    if cluster["name"] == name:
        num = cluster["number"]
    elif cluster["number"] == int(name):
        num = int(name)
if num != None:
    api_urls.append(api_urls[1]+str(num))
    subclusters_json = getData(api_urls[2])
    print(getData(api_urls[2]))
    print("SUBCLUSTERS")
    for subcluster in subclusters_json:
        print(subcluster["name"]+" "+str(subcluster["number"]))
    subname = input("Subcluster name? ")
    for subcluster in subclusters_json:
        if subcluster["name"] == subname:
            subnum = subcluster["number"]
        elif subcluster["number"] == int(subname):
            subnum = subname
    if subnum != None:
        api_urls.append(api_urls[0]+getData(api_urls[0],jsonCat="stations_in_subcluster")[:-20]+str(subnum)+"/")
        api_urls[3] = api_urls[3].strip("/{subcluster_number}")
        print(api_urls[3])
        print(getData(api_urls[3]))
        station_json = getData(api_urls[3])
        for station in station_json:
            print(station["name"]+" "+str(station["number"]))
        stationname = input("Station name: ")
        for station in station_json:
            if station["name"] == stationname:
                stationnum = station["number"]
            elif station["number"] == int(stationname):
                stationnum = stationname
        if stationnum != None:
            station_url = api_urls[0]+"station/"+str(stationnum)
            print(getData(station_url))
            print(getData(station_url+"/config"))

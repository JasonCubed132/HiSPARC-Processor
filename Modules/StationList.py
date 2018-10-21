from tkinter import *
from tkinter import ttk

import json, urllib.request, time
api_urls = ["http://data.hisparc.nl/api/"]
def getData(url,jsonCat = None):
    time_start = time.time()
    print("Attempting request: "+url)
    url = urllib.request.urlopen(url)
    data = json.loads(url.read().decode())
    print(time.time()-time_start)
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
    tree = ttk.Treeview(root,columns=("size","modified"))
def selectItem(a):
    global tree
    curItem = tree.focus()
    item = tree.item(curItem)

def GenRoot(root):
    global tree
    #tree.configure(height=root.size()[1])
    tree = ttk.Treeview(root,columns=("size","modified"))
    tree["columns"] = ("number")
    tree.column("number",width=100)
    tree.heading("number",text="Number")

    api_urls.append(api_urls[0]+getData(api_urls[0],jsonCat="clusters"))
    cluster_json = getData(api_urls[1])
    for cluster in cluster_json:
        #print(cluster["name"]+" "+str(cluster["number"]))
        tree.insert("","end",text=cluster["name"],values=(cluster["number"]))
        Items = tree.get_children()
        cluster_url = api_urls[1]+str(cluster["number"])
        subcluster_json = getData(cluster_url)
        for subcluster in subcluster_json:
            tree.insert(Items[-1],"end",text=subcluster["name"],values=(subcluster["number"]))
            Items2 = tree.get_children(Items[-1])
            subcluster_url = api_urls[0]+getData(api_urls[0],jsonCat="stations_in_subcluster")[:-20]+str(subcluster["number"])+"/"
            stations_json = getData(subcluster_url)
            for station in stations_json:
                tree.insert(Items2[-1],"end",text=station["name"],values=(station["number"]))
    tree.bind('<ButtonRelease-1>', selectItem)
    #tree.insert("","end",text = "Name",values = ("Date","Time","Loc"))
    #tree.insert("I001","end",text = "Name 2",values = ("Date1","Time1","Loc1"))
    #Items = tree.get_children()
    FullStationTree = {}
    ItemsMain = tree.get_children()
    for item in ItemsMain:
        FullStationTree[item] = {}
        ItemsSub = tree.get_children(item)
        for itemSub in ItemsSub:
            FullStationTree[item][itemSub] = {"number":tree.item(itemSub)["values"][0],"name":tree.item(itemSub)["text"]}
    #print(ItemsMain)
    #print(FullStationTree)
    return tree
    #print(Items)

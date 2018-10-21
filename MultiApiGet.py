from multiprocessing import Pool
import requests

def get_data(i):
    r1 = requests.get("http://data.hisparc.nl/api/station/"+str(i))
    a = r1.json()
    return a
terms = [501,502,14006,14001]
print("Start")
#print(get_data(501))
with Pool() as p:
    print("Go")
    print(p.map(get_data,terms))
    print("Go2")

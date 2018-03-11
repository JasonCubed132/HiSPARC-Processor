import requests
response = requests.get("http://data.hisparc.nl/data/301/events?end=2012-02-28&start=2012-01-01&download=False",stream=True)
size = len(response.content)
print(size)

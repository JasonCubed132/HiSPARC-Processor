import requests
#"http://data.hisparc.nl/data/301/events?download=False&end=2012-02-28&start=2012-01-01"
def getSize(url):
    response = requests.get(url, stream=True)
    size = 0
    for chunk in response.iter_content(chunk_size=1024):
        size = size + 1024
    return size

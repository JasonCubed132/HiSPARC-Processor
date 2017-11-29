from urllib2 import urlopen
from datetime import date, timedelta
from pylab import plot, show
id = 501
datum = date(2010, 10, 1)
end_datum = date(2011, 2, 1)
base = 'http://data.hisparc.nl/api/station/%d/num_events/%d/%d/%d'
events = []
dates = []
while datum < end_datum:
     url = urlopen(base % (id, datum.year, datum.month, datum.day))
     events.append(url.read())
     dates.append(datum)
     datum += timedelta(days=1)
step(dates, events)
show()

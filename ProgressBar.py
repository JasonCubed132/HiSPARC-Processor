import requests
import datetime
import urllib
from tkinter import *
import tkinter.ttk as ttk
window = Tk()
def download():
    start_y = 2012
    start_m = 9
    start_d = 1
    end_y = 2012
    end_m = 10
    end_d = 28
    station_id = 301
    print("setted vars")
    date_start = datetime.date(start_y,start_m,start_d) #defines the start date using the given variables
    date_end = datetime.date(end_y,end_m,end_d) #defines the end date using the given variables
    url = "http://data.hisparc.nl/data/{0}/events".format(station_id) #defines the url needed to download the data, this is also where the station_id is used.
    query = urllib.parse.urlencode({"download":False,"start":date_start,"end":date_end}) #gets stuff to add to url. Converts the given data to HTML query format.
    full_url = url + "?" + query #assembles final url for file
    file_url = full_url
    print(file_url)
    print("getting request")
    r = requests.get(file_url)
    size = int(r.head['Content-Length'].strip())
    print(size)
    Bytes = 0 
    widgets = [name, ": ", Bar(marker="|", left="[", right=" "),
        Percentage(), " ",  FileTransferSpeed(), "] ",
        window,
        " of {0}MB".format(str(round(size / 1024 / 1024, 2))[:4])]
    pbar = ttk.ProgressBar(widgets=widgets, maxval=size).start()
    file = []
    print("Bar loaded")
    for buf in r.iter_content(1024):
        if buf:
            print("Iter")
            file.append(buf)
            Bytes += len(buf)
            pbar.update(Bytes)
    pbar.finish()
downloadButton = Button(text="download",command=download)
downloadButton.grid(row=1,column=1)
window.mainloop()

"""try:
  import Tkinter              # Python 2
  import ttk
except ImportError:
  import tkinter as Tkinter   # Python 3
  import tkinter.ttk as ttk


def main():

  root = Tkinter.Tk()

  ft = ttk.Frame()
  fb = ttk.Frame()

  ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  fb.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

  pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')
  pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
  pb_vd = ttk.Progressbar(fb, orient='vertical', mode='determinate')
  pb_vD = ttk.Progressbar(fb, orient='vertical', mode='indeterminate')

  pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  pb_hD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  pb_vd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)
  pb_vD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)

  pb_hd.start(50)
  pb_hD.start(50)
  pb_vd.start(50)
  pb_vD.start(50)

  root.mainloop()

if __name__ == '__main__':
  main()
"""

#Test command:
#python DataDownloader.py -station_id 301 -start_y 2015 -start_m 1 -start_d 1 -end_y 2015 -end_m 12 -end_d 31

#This handles installing and importing modules if needed.
#Check if this is event possible
#Informs the user if pip is not present
try: #Tries the code
    import pip #imports pip
except: #handles any errors
    print("Pip is not installed, this indicates that your python install may be broken, please fix and reload the script.") # prints a message
def install(package): # defines an install method, allows one-line installs later
    pip.main(["install",package]) # runs module install through pip.
modules = ["requests","os","datetime","urllib"] # defines modules to install
for module in modules: # iterates through modules
    try: # tries code
        globals()[module] = __import__(module) #method of importing using string names
    except: # handles errors
        choice = input("{0} is not installed, do you wish to install?") #prompts the user if they want to install or not
        choice = choice.lower() #converts input to lowercase.
        if "y" in choice: #checks if "y" is in the input
            print("Installing...") #tells the user that it's installing
            install(module) #installs the request module
        elif "n" in choice: #checks if "n" is in the input
            print("Canceled, this program cannot continue without this module. Goodbye.") #informs the user that they have cancelled.
            exit() #exits the program.
        else: #handles if both conditions above are false.
            print("Unknownn input, exiting.") #infoms the user that it is exiting.
            exit() #exits the program


#Defines the download function (with arguments.)
def download(station_id,start_y,start_m,start_d,end_y,end_m,end_d):
    print("Setting up directories....") #Informs user
    downloadDir = "\HiSPARC\\" #sets download directory
    os.system("mkdir " + downloadDir) #creates folder for downloads.
    date_start = datetime.date(start_y,start_m,start_d) #defines the start date using the given variables
    date_end = datetime.date(end_y,end_m,end_d) #defines the end date using the given variables
    url = "http://data.hisparc.nl/data/{0}/events".format(station_id) #defines the url needed to download the data, this is also where the station_id is used.
    query = urllib.parse.urlencode({"download":False,"start":date_start,"end":date_end}) #gets stuff to add to url. Converts the given data to HTML query format.
    full_url = url + "?" + query #assembles final url for file
    print("Url assembly done, streaming file to disk, this may take a while...") #informs the user
    response = requests.get(full_url,stream=True) #This creates a request that we can access the data from
    with open(downloadDir+"station{0}-{1}{2}{3}_{4}{5}{6}.csv".format(station_id,start_y,start_m,start_d,end_y,end_m,end_d), 'wb') as handle: #this opens an approprately named file in write bytes mode
        for block in response.iter_content(1024): #this loops through the data in 1024 byte chunks.
            handle.write(block) #this writes that chunk to the file.
if __name__ == "__main__": #called if the file is run directly
    import sys #import to handle the arguments.
    print(sys.argv) #outputs the arguments (for testing purposes)
    Args = sys.argv #gets arguments.
    ProcArgs = [] #creates a new list for the processed arguments.
    for i in range(1,len(Args)-1): #loops through arguments
        if i > len(Args): #checks if the for loop has gone outside of the Args list, this should never happen
            break #exits for loop
        if "-" in Args[i]: #checks if a given argument is a defining tag
            if "-" not in Args[i+1]: # checks if the argument immediately after is a data arg.
                ProcArgs.append([Args[i],Args[i+1]]) #appends the group to processed args.
            else:
                print("No data value specified for {0}, it will be ignored.".format(Args[i])) #this ignores a tag if it has no data.
                #ProcArgs.append(Args[i])
        else:
            continue #This will occur if it checks a data arg as a defining tag.
    #Make sure arguments are there: 
    print(ProcArgs)
    arguments = ["-station_id","-start_y","-start_m","-start_d","-end_y","-end_m","-end_d"] #defines the format for the arguments
    for arg in ProcArgs: #goes through all previous arguments
        for tag in range(0,len(arguments)): #iterates through format
            if arg[0] == arguments[tag]: #tests if procarg value is an int, if so, assign it to its spot in the template.
                try: #tries the code
                    arguments[tag] = int(arg[1]) #tests for int and overwrites it.
                except: 
                    print("{0}: Not a number".format(arg[0])) #output error.
                    exit() #Exits the program if error in arguments.
    print(arguments)
    #Assigns arguments in list to their respective variables
    station_id,start_y,start_m,start_d,end_y,end_m,end_d = arguments[0],arguments[1],arguments[2],arguments[3],arguments[4],arguments[5],arguments[6]
    download(station_id,start_y,start_m,start_d,end_y,end_m,end_d) # executes the download function.
#Test Code - Graveyard.
    """handle = open("\HiSPARC\station{0}-{1}{2}{3}_{4}{5}{6}.csv".format(station_id,start_y,start_m,start_d,end_y,end_m,end_d),"wb")
    #print(response.content)
    handle.write(bytes(full_url,"utf-8"))
    handle.write(response.content)
    print("Written")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)
    handle.close()
    print("File closed")"""
    """url = "http://data.hisparc.nl/data/{0}/events".format(station_id)
    print(url)
    query = urllib.parse.urlencode({"download":False,"start":date_start,"end":date_end})
    print(query)
    full_url = url + "?" + query
    print(full_url)
    #This takes the longest :)
    data = urllib.request.urlopen(full_url).read()
    file = open("station{0}-{1}{2}{3}_{4}{5}{6}.csv".format(station_id,start_y,start_m,start_d,end_y,end_m,end_d),"w")
    file.write(data)
    file.close()"""
    """dates = [date_start + timedelta(days=x) for x in range((date_end-date_start).days + 1)]
    dates_proc = []
    for date in dates:
        print(date)
        date = str(date).split("-")
        dates_proc.append(date)
    print(dates)
    print(dates_proc)
    for date in dates_proc:
        #url = "http://data.hisparc.nl/show/source/eventtime/{0}/{1}/{2}/{3}/".format(station_id,date[0],date[1],date[2])
        url = "http://data.hisparc.nl/api/station/{0}/num_events/{1}/{2}/{3}/".format(station_id,date[0],date[1],date[2])
        response = requests.get(url,stream=True)
        filename = "/HiSPARC/station{0}-{1}{2}{3}.txt".format(station_id,date[0],date[1],date[2])
        handle = open(filename,"wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                handle.write(chunk)
        handle.close()
    print("Done")"""
"""try:
    from datetime import datetime
    #from urllib import urlencode
    import urllib
    from StringIO import StringIO
    from numpy import genfromtxt
except:
    choice = input("Numpy module not found, install?")
    choice = choice.lower()
    if "y" in choice:
        print("Installing...")
        os.system("pip install numpy")
    elif "n" in choice:
        print("Canceled")
        exit()
    else:
        print("Wat.")
        exit()"""
#Year,month,day,hour,minute,second,time zone
    #start_dt = [start_y,start_m,start_d,0,0,0,0,timeZone]
    #end_dt = [end_y,end_m,end_d,23,0,0,0,timeZone]
    #start_date = datetime.datetime(look up module help)
"""#Goes through required modules and checks if present.
try: #tries code
    import requests #this is the module that actually downloads the data.
except: #handles errors.
    choice = input("Requests module not found, install?") #prompts the user if they want to install or not
    choice = choice.lower() #converts input to lowercase.
    if "y" in choice: #checks if "y" is in the input
        print("Installing...") #tells the user that it's installing
        install("requests") #installs the request module
    elif "n" in choice: #checks if "n" is in the input
        print("Canceled, this program cannot continue without this module. Goodbye.") #informs the user that they have cancelled.
        exit() #exits the program.
    else: #handles if both conditions above are false.
        print("Unknownn input, exiting.") #infoms the user that it is exiting.
        exit()"""
"""die = 0
    try:
        station_id = int(station_id)
    except:
        print("Station id not present!")
        die = 1
    try:
        start_y = int(start_y)
    except:
        print("Start year not present!")
        die = 1
    try:
        start_m = int(start_m)
    except:
        print("Start month not present!")
        die = 1
    try:
        start_d = int(start_d)
    except:
        print("Start date not present!")
        die = 1
    try:
        end_y = int(end_y)
    except:
        print("End year not present!")
        die = 1
    try:
        end_m = int(end_m)
    except:
        print("End month not present!")
        die = 1
    try:
        end_d = int(end_d)
    except:
        print("End date not present!")
        die = 1"""
"""for i in range(len(ProcArgs)):
        print(ProcArgs[i-1])
        if "-station_id" in ProcArgs[i-1][0]:
            print("station id detected: {0}".format(ProcArgs[i-1][1]))
            try:station_id = int(ProcArgs[i-1][1])
            except: print("Station ID: Not a number.")
        elif "-start_y" in ProcArgs[i-1][0]:
            print("start_y detected: {0}".format(ProcArgs[i-1][1]))
            try:start_y = int(ProcArgs[i-1][1])
            except: print("Start year: Not a number.")
        elif "-start_m" in ProcArgs[i-1][0]:
            print(" start_m detected: {0}".format(ProcArgs[i-1][1]))
            try:start_m = int(ProcArgs[i-1][1])
            except: print("Start month: Not a number.")
        elif "-start_d" in ProcArgs[i-1][0]:
            print("start_d detected: {0}".format(ProcArgs[i-1][1]))
            try:start_d = int(ProcArgs[i-1][1])
            except: print("Start day: Not a number.")
        elif "-end_y" in ProcArgs[i-1][0]:
            print("end_y detected: {0}".format(ProcArgs[i-1][1]))
            try:end_y = int(ProcArgs[i-1][1])
            except: print("End year: Not a number.")
        elif "-end_m" in ProcArgs[i-1][0]:
            print("end_m detected: {0}".format(ProcArgs[i-1][1]))
            try:end_m = int(ProcArgs[i-1][1])
            except: print("End month: Not a number.")
        elif "-end_d" in ProcArgs[i-1][0]:
            print("end_d detected: {0}".format(ProcArgs[i-1][1]))
            try:end_d = int(ProcArgs[i-1][1])
            except: print("End day: Not a number.")
        else:
            print("Unknown argument detected: {0} = {1}".format(ProcArgs[i-1][0],ProcArgs[i-1][1]))
    if len(ProcArgs) != 7:
        print("Warning, some arguments are missing, please fix.")"""

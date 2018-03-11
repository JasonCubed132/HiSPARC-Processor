#Test command:
#python DataDownloader.py -station_id 301 -start_y 2015 -start_m 1 -start_d 1 -end_y 2015 -end_m 12 -end_d 31

#This handles installing and importing modules if needed.
#Check if this is event possible
#Informs the user if pip is not present
try: #Tries the code
    import pip #imports pip
except: #handles any errors
    print("Pip is not installed, this indicates that your python install may be broken, falling back to windows install method.") # prints a message
def install(package): # defines an install method, allows one-line installs later
    try:
        pip.main(["install",package]) # runs module install through pip.
    except NameError:
        import os
        os.system("pip install "+package)
modules = ["requests","os","datetime","urllib"] # defines modules to install
for module in modules: # iterates through modules
    try: # tries code
        globals()[module] = __import__(module) #method of importing using string names
    except: # handles errors
        choice = input("{0} is not installed, do you wish to install?".format(module)) #prompts the user if they want to install or not
        choice = choice.lower() #converts input to lowercase.
        if "y" in choice: #checks if "y" is in the input
            print("Installing...") #tells the user that it's installing
            install(module) #installs the request module
            globals()[module] = __import__(module) #method of importing using string names
        elif "n" in choice: #checks if "n" is in the input
            print("Canceled, this program cannot continue without this module. Goodbye.") #informs the user that they have cancelled.
            exit() #exits the program.
        else: #handles if both conditions above are false.
            print("Unknownn input, exiting.") #infoms the user that it is exiting.
            exit() #exits the program


#Defines the download function (with arguments.)
def download(station_id,start_y,start_m,start_d,end_y,end_m,end_d,progress=False,barWidget=None):
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
    print(response) #informs of any status codes
    print(downloadDir+"station{0}-{1}{2}{3}_{4}{5}{6}.csv".format(station_id,start_y,start_m,start_d,end_y,end_m,end_d)) #print output file
    if progress == True:
        size = int(response.head['Content-Length'].strip())
        sizeDone = 0
    #This makes sure that the name data for the file names will read correctly.
    while len(str(start_y)) < 4:
        start_y = "0" + str(start_y)
    while len(str(start_m)) < 2:
        start_m = "0" + str(start_m)
    while len(str(start_d)) < 2:
        start_d = "0" + str(start_d)
    while len(str(end_y)) < 4:
        end_y = "0" + str(end_y)
    while len(str(end_m)) < 2:
        end_m = "0" + str(end_m)
    while len(str(end_d)) < 2:
        end_d = "0" + str(end_d)
    with open(downloadDir+"station{0}-{1}{2}{3}_{4}{5}{6}.csv".format(station_id,start_y,start_m,start_d,end_y,end_m,end_d), 'wb') as handle: #this opens an approprately named file in write bytes mode
        for block in response.iter_content(1024): #this loops through the data in 1024 byte chunks.
            handle.write(block) #this writes that chunk to the file.
    response.close()
    print("File stream complete.")
if __name__ == "__main__": #called if the file is run directly
    import sys #import to handle the arguments.
    try: # tries code
        Args = sys.argv #gets arguments.
    except: #run if errored
        print("No arguments detected, manual data input required:") #inform user
        Args = [] #declares arguments if errored.
        arguments = ["-start_y","-start_m","-start_d","-end_y","-end_m","-end_d","-station_id",] #defines the format for the arguments
        for arg in arguments:#iterates through the args.
            print(arg)
            Args.append(arg) #appends arg name to Args, this allows it to be processed as if the args were passed in the cmd line.
            Args.append(input(arg + ": ")) #Appends the data input to the args.
    if len(Args) == 1: #if no arguments are present
        print("No arguments detected, manual data input required:") #inform user
        Args = [] #declares arguments if errored.
        arguments = ["-start_y","-start_m","-start_d","-end_y","-end_m","-end_d","-station_id"] #defines the format for the arguments
        for arg in arguments: #iterates through the args.
            print(arg)
            Args.append(arg) #appends arg name to Args, this allows it to be processed as if the args were passed in the cmd line.
            Args.append(input(arg + ": ")) #Appends the data input to the args.
        print(Args)
    ProcArgs = [] #creates a new list for the processed arguments.
    for i in range(0,len(Args)-1): #loops through arguments and skips first argument
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
    

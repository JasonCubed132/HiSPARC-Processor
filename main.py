#This is the framework code for the processor.
#Import all modules:
print("Begin import")
from Modules import SummerWinter,dataSummary,WriteSummaryToFile,DayNightVariation,DataDownloaderFinal,FileSize
print("Next import.")
import subprocess
print("""This is my main code for processing HiSPARC data.
Unfortunately the program can only handle start and end dates
within the same month. I plan to fix this eventually.""")
downloadDir = "\\HiSPARC\\"
GUI = True
def OpenFile():
        while True:
                try:
                        fileName = input("File name: ")
                except KeyboardInterrupt:
                        print("Exiting.")
                        break
                try:
                        fileData = open(fileName,"r")
                        break
                except FileNotFoundError:
                        print("File not found.")
        fileNameOpen = fileName
        fileName = fileName.strip(".csv")
        fileName = fileName.strip(".tsv")
        print(fileName)
        fileName = fileName.split("-")
        print(fileName)
        fileName.pop(0)
        print(fileName)
        fileName[1] = fileName[1].split("_")
        print(fileName)
        dayStart = fileName[1][0]
        dayEnd = fileName[1][1]
        dayRest = dayStart[:4]+"-"+dayStart[4:-2]+"-"
        dayStart = int(dayStart[6:])
        dayEnd = int(dayEnd[6:])-1
        print(dayRest)
        print(dayStart)
        print(dayEnd)
        return dayRest,dayStart,dayEnd,fileNameOpen
if GUI == False:
    while True:
        print("This is the main menu for the program: ")
        print(" ")
        print("0) Download new data.")
        print("1) Generate summary data for an events file.")
        print("2) Generate summary data and output to a file.")
        print("3) Convert summary data to a file.")
        print("4) Generate day night variation data for summary data.(requires summary data input)")
        print("5) Do both 1 and 4.")
        print("6) Summer winter variation.")
        print("More analysis to be added.")
        print(" ")
        try:
            option = int(input("Please choose an option: "))
        except KeyboardInterrupt:
            break
        except:
            print("Invalid number.")
            continue
        if option == 0:
            print("This program will now download new data (inputs required):")
            inputs = ["station_id","start_y","start_m","start_d","end_y","end_m","end_d"]
            def inputNum(Arg):
                while True:
                    try:
                        return int(input(Arg+": "))
                    except KeyboardInterrupt:
                        return "BREAK"
                    except:
                        print("Error")
                        continue
            for i in range(len(inputs)):
                inputs[i] = inputNum(inputs[i])
                if inputs[i] == "BREAK":
                    break
            DataDownloaderFinal.download(inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5],inputs[6])
        elif option == 1:
            dayRest,dayStart,dayEnd,fileNameOpen = OpenFile()
            print("This program will now calculate the summary data and print out the resulting array.")
            dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
            print(dataSummaryMain)
        elif option == 2:
            print("This program will now calculate the summary data and output it to a file.")
            print("The file name takes the following example format: events-s21-20171010_20171017.tsv")
            dayRest,dayStart,dayEnd,fileNameOpen = OpenFile()
            dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
            WriteSummaryToFile.WriteSummaryToFile(fileNameOpen,dataSummaryMain,dayEnd-dayStart,downloadDir)
        elif option == 3:
            print("Please input the summary data as an array: ")
            dataSummaryMain = input(":")
            print("The file name takes the following example format: events-s21-20171010_20171017.tsv")
            dayRest,dayStart,dayEnd,fileNameOpen = OpenFile()
            WriteSummaryToFile.WriteSummaryToFile(fileNameOpen,dataSummaryMain,dayEnd-dayStart,"\\HiSPARC\\")
        elif option == 4:
            print("Please input the summary data as an array: ")
            dataSummaryMain = input(":")
            TrueFalse= DayNightVariation.DayNightVariation(dataSummaryMain,dayEnd-dayStart)
            print(TrueFalse)
        elif option == 5:
            print("This program will now calculate the summary data and determine whether is has statistically significant variation.")
            dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
            TrueFalse = DayNightVariation.DayNightVariation(dataSummaryMain,dayEnd-dayStart)
            print(TrueFalse)
            #Observations: You should observe that the recorded number of events during the day is slightly smaller in comparison to this during the night.
        elif option == 6:
            print("This program will now calculate the summer winter variation for the given data.")
            print("Please make sure the file contains a whole number of years.")
            dayRest,dayStart,dayEnd,fileNameOpen = OpenFile()
            dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
            SummerWinter.calcVariation(dataSummary,dayRest,dayStart,dayEnd)
        else:
            break
elif GUI == True:
    def load():
        import datetime
        global dayRest,dayStart,dayEnd,fileNameOpen,fileNameEntry,StatusFile,dateStart,dateEnd
        fileName = fileNameEntry.get()
        while True:
            try:
                fileData = open(fileName,"r")
                StatusFile.configure(text="File load OK!")
                break
            except FileNotFoundError:
                StatusFile.configure(text="File not found.")
                return 0
        fileNameOpen = fileName
        fileParts = fileName.split("\\")
        fileName = fileParts[len(fileParts)-1]
        print(fileName)
        fileName = fileName.replace(".csv","")
        fileName = fileName.split("-")
        print(fileName)
        fileName[1] = fileName[1].split("_")
        dayStart = fileName[1][0]
        dayEnd = fileName[1][1]
        dayRest = dayStart[:4]+"-"+dayStart[4:-2]+"-"
        #dayRestStart = dayStart[:4]+"-"+dayStart[4:-2]+"-"
        #dayRestEnd = dayEnd[:4]+"-"+dayEnd[4:-2]+"-"
        dayStart = int(dayStart[6:])
        dayEnd = int(dayEnd[6:])-1
        #dayStartStr = str(dayStart)
        #dayEndStr = str(dayEnd)
        #if len(dayStartStr) < 2:
            #dayStartStr = "0"+dayStartStr
        #if len(dayEndStr) < 2:
            #dayEndStr = "0"+dayEndStr
        #dateStart = datetime.datetime.strptime("%Y-%m-%d",dayRestStart+str(dayStartStr))
        #dateEnd = datetime.datetime.strptime("%Y-%m-%d",dayRestEnd+str(dayEndStr))
        dateStart = datetime.datetime.strptime(fileName[1][0],"%Y%m%d")
        dateEnd = datetime.datetime.strptime(fileName[1][1],"%Y%m%d")
        #\HiSPARC\station301-20140101_20161231.csv
    def SumData():
        global dayRest,dayStart,dayEnd,fileNameOpen,StatusSum,dataSummaryMain,dateStart,dateEnd
        #try:
        dataSummaryMain = dataSummary.ConvertToSummary2(fileNameOpen,dateStart,dateEnd)
        StatusSum.configure(text="Data summary OK!")
        #except:
           # StatusSum.configure(text="Error")

    def SunSave():
        global dayRest,dayStart,dayEnd,fileNameOpen,StatusSum,dataSummaryMain,dateStart,dateEnd
        WriteSummaryToFile.WriteSummaryToFile2(fileNameOpen,dataSummaryMain,dateStart,dateEnd,downloadDir)
        StatusSum.configure(text="Summary write OK!")
    def TextEntry(row,column,window,width=10,height=5):
        frameTemp = Frame(window,width=width,height=height)
        frameTemp.grid(row=row,column=column)
        inputText = Entry(frameTemp)
        inputText.grid(row=row,column=column)
        return frameTemp,inputText
    def SpawnText(row,column,text,window):
        tempText = Label(text=text,width=20)
        tempText.grid(row=row,column=column)
        return tempText
    def SpawnEntryRow(row,startCol,colSize,text,window):
        tempLine = [SpawnText(row,startCol,text,window),TextEntry(row,startCol+colSize,window,width=20)]
        return tempLine
    def lenCheck(text,length,adjust):
        if len(text) < length:
            text = adjust + text
        return text
    def downloadMethod(station_id,start_y,start_m,start_d,end_y,end_m,end_d,progress=False,barWidget=None):
        import os
        import datetime
        import urllib
        import requests
        import urllib.request
        print("Setting up directories....") #Informs user
        downloadDir = "\HiSPARC\\" #sets download directory
        os.system("mkdir " + downloadDir) #creates folder for downloads.
        date_start = datetime.date(start_y,start_m,start_d) #defines the start date using the given variables
        date_end = datetime.date(end_y,end_m,end_d) #defines the end date using the given variables
        url = "http://data.hisparc.nl/data/{0}/events".format(station_id) #defines the url needed to download the data, this is also where the station_id is used.
        query = urllib.parse.urlencode({"download":False,"start":date_start,"end":date_end}) #gets stuff to add to url. Converts the given data to HTML query format.
        full_url = url + "?" + query #assembles final url for file
        print(full_url)
        print("Url assembly done, streaming file to disk, this may take a while...") #informs the user
        response = requests.get(full_url,stream=True) #This creates a request that we can access the data from
        print(response) #informs of any status codes
        print(downloadDir+"station{0}-{1}{2}{3}_{4}{5}{6}.csv".format(station_id,start_y,start_m,start_d,end_y,end_m,end_d)) #print output file
        if progress == True:
            size = FileSize.getSize(full_url)
            sizeDone = 0
            Progress["value"] = 0
            Progress["maximum"] = size
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
                if progress == True:
                    sizeDone = sizeDone + 1024
                    Progress["value"] = sizeDone
        response.close()
        print("File stream complete.")
    def download():
        import datetime,urllib,requests
        stationID = str(stationLine[1][1].get())
        startY = str(startYLine[1][1].get())
        startM = str(startMLine[1][1].get())
        startM = lenCheck(startM,2,"0")
        startD = str(startDLine[1][1].get())
        startD = lenCheck(startD,2,"0")
        endY = str(endYLine[1][1].get())
        endM = str(endMLine[1][1].get())
        endM = lenCheck(endM,2,"0")
        endD = str(endDLine[1][1].get())
        endD = lenCheck(endD,2,"0")
        date_start = datetime.date(int(startY),int(startM),int(startD)) #defines the start date using the given variables
        date_end = datetime.date(int(endY),int(endM),int(endD)) #defines the end date using the given variables
        url = "http://data.hisparc.nl/data/{0}/events".format(stationID) #defines the url needed to download the data, this is also where the station_id is used.
        query = urllib.parse.urlencode({"download":False,"start":date_start,"end":date_end}) #gets stuff to add to url. Converts the given data to HTML query format.
        full_url = url + "?" + query #assembles final url for file
        #req = requests.get(full_url,stream=True)
        subprocessTrigger = True
        
        DownloadInfo.configure(text="Info parse OK!")
        fileName = "\\HiSPARC\\"+"station"+stationID+"-"+startY+startM+startD+"_"+endY+endM+endD+".csv"
        fileNameEntry.delete(0,END)
        fileNameEntry.insert(0,fileName)
        DownloadInfo.configure(text="File name insert OK!")
        if subprocessTrigger == True:
            inputs = ["python","Modules/DataDownloaderFinal.py","-station_id",stationID,"-start_y",startY,"-start_m",startM,"-start_d",startD,"-end_y",endY,"-end_m",endM,"-end_d",endD,"-progress"]
            cmd = ""
            #for item in inputs:
                #cmd = cmd + " " + item
            
            #size = FileSize.getSize(full_url)
            #size = len(req.content)
            #sizeDone = 0
            #Progress["value"] = 0
            #Progress["maximum"] = size
            DownloadInfo.configure(text="Cmd build OK!")
            DownloadInfo.configure(text="Download start OK!")
            process = subprocess.Popen(inputs,stdout=subprocess.PIPE,shell=False)
            """for block in response.iter_content(1024):
                sizeDone = sizeDone + 1024
                Progress["value"] = sizeDone"""
                
        elif subprocessTrigger == False:
            downloadMethod(int(stationID),int(startY),int(startM),int(startD),int(endY),int(endM),int(endD),progress=True,barWidget=Progress)
        #DownloadInfo.configure(text="Download OK!")
        load()
        #DownloadInfo.configure(text="Auto load OK!")
    def dayNightVar():
        global dataSummaryMain,dayRest,dayStart,dayEnd,fileNameOpen
        if dataSummaryMain == None:
            dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
        TrueFalse = DayNightVariation.DayNightVariation2(dataSummaryMain,dayEnd-dayStart)
        
    try:
        from Tkinter import *
    except ImportError:
        from tkinter import *
        from tkinter import ttk
    window = Tk()
    window.title("HiSPARC Data processor.")
    frame = Frame(window,width=20)
    frame.grid(row=1,column=1)
    fileNameEntry = Entry(frame,text="defualt.txt",width=20)
    fileNameEntry.grid(row=1,column=1)
    loadFile = Button(command=load,text="Load File",width=20)
    loadFile.grid(row=1,column=10)
    StatusFile = Label(text="Waiting..",width=20)
    StatusFile.grid(row=1,column=20)
    Summarise = Button(text="Generate summary data.",command=SumData,width=20)
    Summarise.grid(row=2,column=1)
    SaveSum = Button(text="Save summary data to file.",command=SunSave,width=20)
    SaveSum.grid(row=2,column=10)
    StatusSum = Label(text="Waiting..")
    StatusSum.grid(row=2,column=20)
    stationLine = SpawnEntryRow(3,1,9,"Station ID: ",window)
    startYLine = SpawnEntryRow(4,1,9,"Start Year: ",window)
    startMLine = SpawnEntryRow(5,1,9,"Start Month: ",window)
    startDLine = SpawnEntryRow(6,1,9,"Start Day: ",window)
    endYLine = SpawnEntryRow(7,1,9,"End Year: ",window)
    endMLine = SpawnEntryRow(8,1,9,"End Month: ",window)
    endDLine = SpawnEntryRow(9,1,9,"End Day: ",window)
    Download = Button(text="Download",command=download,width=20)
    Download.grid(row=10,column=1)
    DownloadInfo = Label(text="Waiting...")
    DownloadInfo.grid(row=10,column=20)
    #Progress = ttk.Progressbar(window,orient="horizontal",length=200,mode="determinate")
    #Progress.grid(row=11,column=1,columnspan=20)
    DayNightButton = Button(command=dayNightVar,text="Get day night variation.",width=20)
    DayNightButton.grid(row=11,column=1)
    DayNightStatus = Label(text="Waiting...",width=20)
    DayNightStatus.grid(row=11,column=20)
    DayNightVari = Label(text="Day night variation data will appear here.",width=40)
    DayNightVari.grid(row=12,column=1,columnspan=19)
    window.mainloop()
    
    
    

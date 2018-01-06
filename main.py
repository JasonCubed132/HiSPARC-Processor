#This is the framework code for the processor.
#Import all modules:
from Modules import dataSummary,WriteSummaryToFile,DayNightVariation
print("""This is my main code for processing HiSPARC data.
This program requires several inputs:

1) The file name (e.g. events-s21-20171010_20171017.tsv).

Unfortunately the program can only handle start and end dates
within the same month. I plan to fix this eventually.""")
while True:
    try:
        fileName = input("File name: ")
    except KeyboardInterrupt:
        print("Exiting.")
    try:
        fileData = open(fileName,"r")
    except FileNotFoundError:
        print("File not found.")
fileNameOpen = fileName
fileName = fileName.replace(".tsv","")
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
while True:
    print("This is the main menu for the program: ")
    print(" ")
    print("1) Generate summary data for an events file.")
    print("2) Generate summary data and output to a file.")
    print("3) Convert summary data to a file.")
    print("4) Generate day night variation data for summary data.(requires summary data input)")
    print("5) Do both 1 and 4.")
    print("More analysis to be added.")
    print(" ")
    try:
        option = int(input("Please choose an option: "))
    except KeyboardInterrupt:
        break
    except:
        print("Invalid number.")
        continue
    if option == 1:
        print("This program will now calculate the summary data and print out the resulting array.")
        dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
        print(dataSummaryMain)
    elif option == 2:
        print("This program will now calculate the summary data and output it to a file.")
        dataSummaryMain = dataSummary.ConvertToSummary(fileNameOpen,dayStart,dayEnd,dayRest)
        WriteSummaryToFile.WriteSummaryToFile(fileNameOpen,dataSummaryMain,dayEnd-dayStart)
    elif option == 3:
        print("Please input the summary data as an array: ")
        dataSummaryMain = input(":")
        WriteSummaryToFile.WriteSummaryToFile(fileNameOpen,dataSummaryMain,dayEnd-dayStart)
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
    else:
        break

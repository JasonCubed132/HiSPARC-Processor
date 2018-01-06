#This is the framework code for the processor.
print("""This is my main code for processing HiSPARC data.
This program requires several inputs:

1) The file name (e.g. events-s21-20171010_20171017.tsv).
2) The start date of the data (YYYY/MM/DD).
3) The end date of the data (YYYY/MM/DD).

Unfortunately the program can only handle start and end dates
within the same month. I plan to fix this eventually.""")
fileName = input("1) ")
#fileData = open(fileName,"r")
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

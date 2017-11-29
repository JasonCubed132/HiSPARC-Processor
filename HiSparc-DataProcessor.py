#GENERAL INPUTS HAVE BEEN COMMENTED OUT TO MAKE TESTING EASIER
fileName = input("File name pls: ")
#fileName = "events-s21-20171010_20171017.tsv"
fileData = open(fileName,"r")
#REPLACE THIS WITH GEN CODE!
#dataSummary = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
dayStart = int(input("Start day pls: "))
#dayStart = 10
dayEnd = int(input("End day pls: "))
#dayEnd = 16
dayRest = input("Please input the start format: (YYYY-MM-)")
#dayRest = "2017-10-"
#RUN LOOP FOR AMOUNT OF DAYS
dataSummary = []
dataDayTemplate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dayLen = (dayEnd - dayStart)+1
data=[]
for i in range(dayLen):
    dataSummary.append(data)
for i in range(dayLen):
    dataTempCopy = dataDayTemplate.copy()
    dataSummary[i] = dataTempCopy
    dataTempCopy = []
print(dataSummary)
#dataSummary = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
for i in range(dayLen):
    #RUN LOOP FOR AMOUNT OF HOURS
    for j in range(24):
        print(str(i) + ":" + str(j))
        a = 0
        #SEARCH THROUGH FILE
        if len(str(j)) == 1:
            TestHour = "0"+str(j)
            #print(TestHour)
        else:
            TestHour = str(j)
        day = str(dayStart+i)
        if len(day) == 1:
            day = "0"+day
        print(dayRest+day+"	"+TestHour)
        for line in fileData:
            #LINE COUNTER - NOT NECESSARY
            a = a + 1
            
            #print(line)
            #DON'T BOTHER TO RUN CODE FOR FIRST ~20 LINES OF FILE
            if "#" in line:
                #print("Skipped")
                holding = 1
            else:
                #print("Not skipped")
                #print(dayRest+str(i)+"	"+str(j))
                #CHECK LINE FOR CORRECT STRING

                if dayRest+day+"	"+TestHour in line:
                    #RECORD THAT EVENT HAS OCCURED IN SUMMARY TABLE
                    dataSummary[i][j] = dataSummary[i][j] + 1
                    #NOT NECESSARY
                    if j == 0:
                        holding = 1
                    else:
                        #print("Event recorded.")
                        holding = 1
                else:
                    print(dataSummary[i][j])
                    break
                    
        if dataSummary[i][j] == 0:
            print("No data recorded")
        #FORCE CURSOR BACK TO START OF FILE
        #fileData.seek(0)
    print(dataSummary)
#OUTPUT SUMMARY DATA
fileData.close()
print(dataSummary)
print(fileName)
fileName = fileName.replace(".tsv","_Summary.txt")
print(fileName)
fileData = open(fileName, "w")
mainString = ""
for i in range(len(dataSummary)):
    subString = ""
    for j in range(24):
        subString = subString + str(dataSummary[i][j]) + ":"
    subString = subString[len(subString)-1:]
    mainString = mainString + subString + ";"
mainString = mainString[len(mainString)-1:]
print(mainString)
"""fileData.write("Summary Data:\n")
fileData.write(dayRest+str(dayStart) + " " + dayRest+str(dayEnd)+"\n")
for i in range(dayLen):
    fileData.write("Data for day: " + str(dayStart + i)+"\n")
    for j in range(24):
        fileData.write(str(dataSummary[i][j])+"\n")"""
for j in range(24):
    for i in range(dayLen):
        print(str(i)+","+str(j))
        fileData.write(str(dataSummary[i][j])+",")
    fileData.write("\n")
fileData.close()

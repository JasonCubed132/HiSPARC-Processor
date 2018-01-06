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

#This next bit is for day night variation of the data:
#Get sum of day in hours 10-14 and night 22-02

dataSum = []
dataSumTemplate = [0,0]
for i in range(dayLen):
    dataSum.append(dataSumTemplate.copy())

#This handles during the day
for i in range(dayLen):
    for j in range(10,14):
        dataSum[i][0] = dataSum[i][0] + dataSummary[i][j]
print(dataSum)

#This handles during the night
for i in range(dayLen):
    for j in range(22,26):
        if j > 23:
            num = j-23
        else:
            num = j
        dataSum[i][1] = dataSum[i][1] + dataSummary[i][num]
print(dataSum)
    
#This gets the average:
dataAvg = [0,0]
for i in range(2):
    for j in range(dayLen):
        dataAvg[i] = dataAvg[i] + dataSum[j][i]
    dataAvg[i] = dataAvg[i]/7
print(dataAvg)

#some difference stuff.
AvgDif = dataAvg[1]-dataAvg[0]
#This is code i got off the internet to calculate standard deviation:
from math import sqrt,pow
 
 
def standard_deviation(lst, population=False):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    mean = sum(lst) / num_items
    differences = [x - mean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
 
    # Note: it would be better to return a value and then print it outside
    # the function, but this is just a quick way to print out the values along
    # the way.
    if population is True:
        #print('This is POPULATION standard deviation.')
        variance = ssd / num_items
    else:
        #print('This is SAMPLE standard deviation.')
        variance = ssd / (num_items - 1)
    sd = sqrt(variance)
    # You could `return sd` here.
    return sd
    """print('The mean of {} is {}.'.format(lst, mean))
    print('The differences are {}.'.format(differences))
    print('The sum of squared differences is {}.'.format(ssd))
    print('The variance is {}.'.format(variance))
    print('The standard deviation is {}.'.format(sd))
    print('--------------------------')"""

#This is the code to handle the standard deviation:
nightDev = standard_deviation(dataSum[1])
dayDev = standard_deviation(dataSum[0])
diffDev = pow((pow(nightDev,2)+pow(dayDev,2)),(1/2))

#Final comparison:
AvgDif5 = AvgDif*5
if AvgDif5 > diffDev:
    print("This time series has statistially significant variation.")
else:
    print("This is not statistically significant variation.")

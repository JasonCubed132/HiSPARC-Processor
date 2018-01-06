#This is the data summary generator:
def ConvertToSummary(fileName,dayStart,dayEnd,dayRest):
    #fileName = "events-s21-20171010_20171017.tsv"
    fileData = open(fileName,"r")
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
    ##print(dataSummary)
    #dataSummary = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    for i in range(dayLen):
        #RUN LOOP FOR AMOUNT OF HOURS
        for j in range(24):
            ##print(str(i) + ":" + str(j))
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
            ##print(dayRest+day+"	"+TestHour)
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
        ##print(dataSummary)
    #OUTPUT SUMMARY DATA
    fileData.close()
    ##print(dataSummary)
    ##print(fileName)
    return dataSummary
if __name__ == "__main__":
    fileName = input("File name pls: ")
    #fileName = "events-s21-20171010_20171017.tsv"
    #dataSummary = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    dayStart = int(input("Start day pls: "))
    #dayStart = 10
    dayEnd = int(input("End day pls: "))
    #dayEnd = 16
    dayRest = input("Please input the start format: (YYYY-MM-)")
    #dayRest = "2017-10-"
    dataSummary = ConvertToSummary(fileName,dayStart,dayEnd,dayRest)
    print(dataSummary)

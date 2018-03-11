#This is the data summary generator:
#\HiSPARC\station301-20150101_20161231.csv
import datetime
def ConvertToSummary(fileName,dayStart,dayEnd,dayRest,method=1):
    if method == 1:
        startDate = dayRest+str(dayStart)
        endDate = dayRest+str(dayEnd)
        startDate = datetime.datetime.strptime(startDate,"%Y-%m-%d")
        endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d")
        dataSummary = []
        dataDayTemplate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        fileData = open(fileName,"r").readlines()
        day_count = (endDate - startDate).days + 1
        pos = 0
        #for single_date in [d for d in (startDate + datetime.timedelta(n) for n in range(day_count)) if d <= endDate]:
        while startDate < endDate:
            print(dataSummary)
            if pos == 0:
                dataSummary = [dataDayTemplate.copy()]
            else:
                dataSummary = dataSummary.append(dataDayTemplate.copy())
            #date = datetime.datetime.strftime("%Y-%m-%d", single_date.timetuple())
            for hour in range(0,23):
                for line in fileData:
                    #print(line)
                    print(str(startDate)[:13])
                    if "#" in line:
                        continue
                    if str(startDate)[:13] in line:
                        print(pos,hour)
                        dataSummary[pos][hour] = dataSummary[pos][hour] + 1
                        print(dataSummary)
                        print("Line check")
                    else:
                        break
                    print("Line check")
                print("Next hour")
                startDate = startDate + datetime.timedelta(hours=1)
            print("Next day")
            pos = pos + 1
            
        fileData.close()
        return dataSummary
                    
    elif method == 2:
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
def ConvertToSummary2(fileName,dayStart,dayEnd):
    #startDate = dayRest+str(dayStart)
    #endDate = dayRest+str(dayEnd)
    #print(startDate)
    #print(endDate)
    #dayStart = datetime.datetime.strptime(startDate,"%Y-%m-%d")
    #dayEnd = datetime.datetime.strptime(endDate,"%Y-%m-%d")
    #print(dayStart)
    #print(dayEnd)
    dayLength = (dayEnd-dayStart).days
    fileData = open(fileName,"r")
    dataSummary = []
    dataDayTemplate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pos = 0
    print(dayLength)
    for i in range(dayLength):
        dataSummary.append(dataDayTemplate.copy())
    hour = 0
    while dayStart < dayEnd:
        #for hour in range(0,23):
            #if len(str(hour)) < 2:
                #test = "0" + str(hour)
            #else:
                #test = str(hour)
            #print(dayStart.strftime("%Y-%m-%d")+"	"+test)
        for line in fileData:
            #print(line)
            if "#" in line:
                print("Skipped")
                continue
            if dayStart.strftime("%Y-%m-%d	%H") in line:
                dataSummary[pos][int(dayStart.strftime("%H"))] += 1
            else:
                print("Next hour")
                break
        #if dayStart.strftime("%Y-%m-%d") not in line:
            #break
        #print("Next day")
        hour = hour + 1
        if hour > 23:
            hour = 0
            pos = pos+1
        dayStart = dayStart + datetime.timedelta(hours=1)
    print(dataSummary)
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

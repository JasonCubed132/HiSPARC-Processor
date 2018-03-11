#Day night variation
#This next bit is for day night variation of the data:
#Get sum of day in hours 10-14 and night 22-02
import datetime
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
def DayNightVariation(dataSummary,dayLen):
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
        return True
    else:
        print("This is not statistically significant variation.")
        return False
def DayNightVariation2(dataSummary,dayStart,dayEnd):
    dataSum = []
    dataSumTemplate = [0,0]
    dayCount = (dayEnd-dayStart).days + 1
    pos = 0
    while dayStart < dayEnd:
        if pos == 0:
            dataSum = dataSumTemplate.copy()
        else:
            dataSum = dataSun.append(dataSumTemplate.copy())
        for i in range(10,14):
            dataSum[pos][0] = dataSum[pos][0] + dataSummary[pos][i]
        for i in range(22,26):
            if i > 23:
                j = i - 23
            else:
                j = i
            dataSum[pos][1] = dataSum[pos][1] + dataSummary[pos][i]
        dayStart = dayStart + datetime.timedelta(days=1)
    dayAvgTemplate = [0,0]
    dayAvg = []
    weeks = len(dataSum)/7
    for i in range(weeks):
        dayAvg = dayAvg.append(dayAvgTemplate)
        for k in range(2):
            for j in range(7):
                currentDay = (weeks*7)+j
                dayAvg[i][k] = dayAvg[i][k] + dataSum[currentDay][k]
    print(dayAvg)
            
    

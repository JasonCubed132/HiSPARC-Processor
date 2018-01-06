#Write data summary to file:
def WriteSummaryToFile(fileName,dataSummary,dayLen):
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
    for j in range(24):
        for i in range(dayLen):
            print(str(i)+","+str(j))
            fileData.write(str(dataSummary[i][j])+",")
        fileData.write("\n")
    fileData.close()
    return None

    

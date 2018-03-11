#Write data summary to file:
def WriteSummaryToFile(fileNameOld,dataSummary,dayLen,downloadDir):
    fileName = fileNameOld.replace(".tsv","_Summary.txt")
    if fileName == fileNameOld:
        fileName = fileName.append("_Summary.txt")
    print(fileName)
    fileData = open(downloadDir+fileName, "w")
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
def WriteSummaryToFile2(fileNameOld,dataSummary,dayStart,dayEnd,downloadDir):
    fileName = fileNameOld.replace(".csv","_Summary.txt")
    fileName = fileName.replace(".tsv","_Summary.txt")
    fileData = open(fileName,"w")
    for i in range(len(dataSummary)):
        for j in range(24):
            if j == 0:
                fileData.write(str(dataSummary[i][j]))
            else:
                fileData.write(","+str(dataSummary[i][j]))
        fileData.write("\n")
    fileData.close()
    return None


    

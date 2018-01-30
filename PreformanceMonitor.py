import os,time,subprocess
while True:
    subprocess.call("tasklist /FO csv > tmp.csv",shell=True)
    data = open("tmp.csv","r")
    data_file = data.readlines()
    for line in data_file:
        if "python" in line:
            line = line.strip("\n")
            line = line.split("\",\"")
            print("{0}\t{1}\t{2}\t{3}\t{4}".format(line[0],line[1],line[2],line[3],line[4]))
    data.close()
    os.remove("tmp.csv")
    print("---------------------------------------------------")
    time.sleep(15)

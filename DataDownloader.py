import os,datetime
#Arguments - self assign for now
downloadDir = "\HiSPARC\"
stationID = 301
start_y = 2015
start_m = 1
start_d = 1
end_y = 2013
end_m = 1
end_d = 31
#This is the arguments parser:
import sys
print(sys.argv)
Args = sys.argv
Args.pop(0)
ProcArgs = []
for i in range(len(Args)-1):
    if i > len(Args):
        break
    #print(i)
    #print(Args)
    #print(ProcArgs)
    if "-" in Args[i]:
        if "-" not in Args[i+1]:
            ProcArgs.append([Args[i],Args[i+1]])
        else:
            print("No data value specified for {0}, I hope it is a flag.".format(Args[i]))
            ProcArgs.append(Args[i])
    else:
        continue
print(Args)
print(ProcArgs)
#Make sure arguments are there:
if station_id in ProcArgs:
    
    print("station id detected: {0}")
#Start of main code.
os.system("mkdir " + downloadDir)
timeZone = "Europe/London"
#Year,month,day,hour,minute,second,time zone
start_dt = [start_y,start_m,start_d,0,0,0,0,timeZone]
end_dt = [end_y,end_m,end_d,23,0,0,0,timeZone]
start_date = datetime.datetime(look up module help)

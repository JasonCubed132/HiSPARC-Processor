import sys
print(sys.argv)
Args = sys.argv
Args.pop(0)
#print(sys.argv)
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
            #Args.pop(i)
            #Args.pop(i)
        #else:
            #Args.pop(i)
        else:
            print("No data value specified for {0}, it will be ignored.".format(Args[i]))
            ProcArgs.append(Args[i])
    else:
        continue
print(Args)
print(ProcArgs)

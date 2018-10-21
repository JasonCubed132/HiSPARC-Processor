import csv
fileName = input("File name: ")
fileNameCsv = fileName.replace(".tsv",".csv")
import re
infile = fileName
outfile = fileNameCsv
ifh = open (infile, 'r')
ofh = open (outfile, 'w+')
for line in ifh:
    if "#" in line:
        continue
    line = line.strip("\n")
    line = re.sub('\t', '","', line)
    ofh.write('"' + line + '"'+"\n")
ifh.close()
ofh.close()
#DATE,TIME,UNIX_TIME,TIMESTAMP,PULSE1,PULSE2,PULSE3,PULSE4,INTEG1,INTEG2,INTEG3,INTEG4,MIPS1,MIPS2,MIPS3,MIPS4,ARRIVE1,ARRIVE2,ARRIVE3,ARRIVE4,TRIGGER,ZENITH,AZIMUTH


fileName = input("Input file name: ")
count = 0
with open(fileName,"r") as die:
    for line in die:
        count = count + 1
    die.close()
print(count)

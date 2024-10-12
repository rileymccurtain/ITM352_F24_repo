with open("Names.txt",mode="r") as textFile:
    line = textFile.readline()
    count = 0

    while line:
        print(line)
        count += 1
        line = textFile.readline()

print (f"There are {count} names in the file")
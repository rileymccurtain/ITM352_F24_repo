with open("Names.txt",mode="r") as textFile:    
    NameList = textFile.read()
    print(type(NameList))
    print(NameList)

SeparatedList = NameList.split("\n")
print(SeparatedList)
count = len(SeparatedList)
print(f"There are {count} names in the file")
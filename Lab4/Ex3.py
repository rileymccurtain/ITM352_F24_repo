#Manipulate a list in various ways 

#responseValues = [5, 7, 3, 8, 0]
#responseValues.append(0)
#responseValues.insert (2,6)

responseValues = responseValues[0:2] + [6] + responseValues[2:]
responseValues.sort()
responseValues.remove(0)

print(responseValues)
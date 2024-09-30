# Program to count letter frequencies in a string 

# Count the frequencies of letters in an input string, ignoring case
def getFrequencies(inString):
    freqDict = {}
    for character in inString:
        character = character.lower()
        if character not in freqDict:
        freqDict[character] = 1
        else:
        freqDict[character] += 1
    return = freqDict

inputString = input("Please enter a string: ")

dict = getFrequencies(inputString)
print(dict)
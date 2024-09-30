# Examine every element of a tuple. 
# Within the loop, use an if statement to count how many of the 
# elements are strings. After the loop completes, print out a message 
# stating how many strings are in the tuple.

Weird = ("hello", 10, "goodbye", 3, "goodnight", 5, "Go away")
numStrings = 0

for x in Weird:
    if (type(x) is str):
        numStrings += 1

print(f"We have {numStrings} strings")
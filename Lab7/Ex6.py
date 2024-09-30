# Append a user-specified value to a tuple

Weird = ("hello", 10, "goodbye", 3, "goodnight", 5, "Go away")

userVal = ("Please enter a value: ")

try:
    Weird[7] = userVal
except:
    print("You can not add elements to a tuple doofus!")
#Ask the user to enter their first name, middle initial, and 
#last name. Concatenate them together with spaces in between 
# and print out the result. 

First = input ("Please enter your first name: ")
MiddleInitial = input ("Please enter your middle initial: ")
Last = input ("Please enter your last name: ")

FullName = First + " " + MiddleInitial + " " + Last
print("Your full name is ", FullName)
print(f"Your full name is {First} {MiddleInitial} {Last}")
print("Your full name is %s %s %s" % (First, MiddleInitial, Last))
print("Your full name is {} {} {}".format (First, MiddleInitial, Last))
print("Your full name is " "".join([First, MiddleInitial + ".", Last]))

name_list = [First, MiddleInitial, Last]

FullName = "{} {} {}".format(*name_list)

print("Your full name is {}".format(FullName))

















a.
#input function
first_name = input ("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

#concatenation
full_name = first_name + " " + middle_initial + " " + last_name

#print
print("Your full name is:", full_name)

b.
#f-string
#input function
first_name = input ("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

#concatenation
full_name = f"{first_name} {middle_initial} {last_name}"

#print
print(f"Your full name is: {full_name}")

c. 
# % operator
#input function
first_name = input ("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

#concatenation
full_name = "%s %s %s" % (first_name, middle_initial, last_name)

#print
print("Your full name is: %s" % full_name)

d. 
#format()
#input function
first_name = input ("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

#concatenation
full_name = "{} {} {}".format(first_name, middle_initial, last_name)

#print
print("Your full name is: {}".format(full_name))

e.
#join()
#input function
first_name = input ("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

#concatenation
full_name = " ".join([first_name, middle_initial, last_name])

#print
print(f"Your full name is: {full_name}")

f. 
#format() method for a string but unpacking the list as the argument
#input function
first_name = input ("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

#list
name_parts = [first_name, middle_initial, last_name]

#concatenation
full_name = "{} {} {}".format(*name_parts)

#print
print("Your full name is: {}".format(full_name))
full_name = "{} {} {}".format(*name_parts)




NameParts = [First, MiddleInitial, Last]

FullName = "{} {} {}".format(*NameParts)

print("Your full name is", FullName)

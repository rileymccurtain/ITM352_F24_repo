Year = int(input("Please enter a year: "))

if(Year % 4 == 0 and Year % 100 != 0) or (Year % 400 == 0):
    print("leap year")
else:
    print("not a leap year")
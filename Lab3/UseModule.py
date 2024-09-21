# Program to test the use of the HandyMath library
import HandyMath as HM

number1 = input ("Enter first value: ")
number2 = float(input("Enter second value: "))
number1 = float(number1)


mid = HM.midpoint (number1, number2)
print(f"The midpoint between {number1} and {number2} is:", {mid})

square = HM.squareroot (number1)
print(f"The square root of {number1} is:", {square})

exponent = HM.exponent (number1, number2)
print(f"The value of raising {number1} to the power of {number2} is:", {exponent})

Max = HM.max (number1, number2)
print(f"The maximum of {number1} and {number2} is:", {max})

Min = HM.min (number1, number2)
print(f"The minimum of {number1} and {number2} is:", {min})

print (HM.exponent.__name__)
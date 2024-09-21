# Library of Handy reusable math functions 

# Given two numbers, returns the midpoint between them 
def midpoint(num1, num2):
    return ((num1 + num2)/2)

# Square Root Function
def squareroot(n):
    return n ** 0.5

# Exponent Function
def exponent (num1, num2):
    return num1 ** num2

# Max Function
def max(num1, num2):
    if num1 > num2:
        return(num1)
    else:
        return(num2)

# Min Function
def min(num1, num2):
    if num1 < num2:
        return(num1)
    else:
        return(num2)
# Ask the user to input a temperature in degrees Fahrenheit. 
# Convert that temperature to Celsius and output it. 

# Function to convert degrees F to degrees C
def FtoC(temperatureF)
    degreeC = (float (degreesF) - 32) * (5/9)
    return(degreesC)

degreesF = input("Enter a temperature in Fahrenheit: ")

print("This converts to ", FtoC(degreesF), "Celsius")
Not part of lab. Example. 
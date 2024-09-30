# Use a while loop to create a list of even numbers from 1 to 50

evenNumbers = []
counter = 1

while counter <= 50:
    if counter % 2 == 0:
        evenNumbers.append(counter)
    counter += 1    

print(evenNumbers)
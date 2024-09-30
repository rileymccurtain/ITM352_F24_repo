# Create a list of elements containing the odd numbers between 1 and 50

oddNumbers = []

#for num in range(1,50):
#    if num % 2 == 1:
#        oddNumbers.append(num)

#for num in range(0,25):
#    oddNumbers.append(2*num+1)

#for num in range(1,50,2):
#    oddNumbers.append(num)

oddNumbers = [x for x in range(1,51) if x % 2 != 0]

print(oddNumbers)
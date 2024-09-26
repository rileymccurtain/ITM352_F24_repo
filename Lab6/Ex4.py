Age = int(input("Please enter your age: "))
Tuesday = input("Is it Tuesday? (yes/no): ").strip().lower() == "yes"
Matinee = input("Is it a matinee? (yes/no): ").strip().lower() == "yes"

price = 14

if Matinee:
    if Age >= 65:
        price = 5  
    else:
        price = 8  
elif Age >= 65:
    price = 8  
elif Tuesday:
    price = 10  

print(f"Age: {Age}")
print(f"Tuesday: {Tuesday}")
print(f"Matinee: {Matinee}")
print(f"Price: ${price}")
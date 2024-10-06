#Debugging exercise # 2
prices = [5.95, 3.00, 12.50]
total_price = 0
tax_rate = .08    # 8% tax 
for price in prices:
    total_price += price
total_price += total_price * tax_rate    

print(f"Total price (with tax): ${round(total_price,2)}")
import csv

total_fare = 0
num_fares = 0
max_trip_miles = 0

with open("/Users/rileymccurtainschool/Downloads/taxi_1000.csv", "r") as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  
    
    for row in csv_reader:
        try:
            fare = float(row[9])
            trip_miles = float(row[4])

            total_fare += fare
            num_fares += 1

            if trip_miles > max_trip_miles:
                max_trip_miles = trip_miles

        except (ValueError, IndexError):
            pass

average_fare = total_fare / num_fares if num_fares > 0 else 0

print(f"Total of all fares: ${total_fare:.2f}")
print(f"Average fare: ${average_fare:.2f}")
print(f"Maximum trip distance: {max_trip_miles} miles")
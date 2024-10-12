import csv
import os

file_path = "/Users/rileymccurtainschool/Downloads/taxi_1000.csv"

if os.path.exists(file_path) and os.access(file_path, os.R_OK):

    total_fare = 0
    num_fares = 0
    max_trip_miles = 0

    with open(file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        for row in csv_reader:
            try:
                fare = float(row[9])
                trip_miles = float(row[4])

                if fare > 10:
                    total_fare += fare
                    num_fares += 1

                    if trip_miles > max_trip_miles:
                        max_trip_miles = trip_miles

            except (ValueError, IndexError):
                print(f"Skipping invalid row: {row}")
                pass

    average_fare = total_fare / num_fares if num_fares > 0 else 0

    print(f"Total of all fares greater than $10: ${total_fare:.2f}")
    print(f"Average fare for fares greater than $10: ${average_fare:.2f}")
    print(f"Maximum trip distance for fares greater than $10: {max_trip_miles} miles")

else:
    print(f"File {file_path} does not exist or is not readable.")
# Create a histogram from the trip miles data
import matplotlib.pyplot as plt
import pandas as pd

# Read the data file and create a DataFrame
trips_df = pd.read_json("../Trips from area 8.json")
trip_miles_series = trips_df.trip_miles

fig = plt.figure() # Not strictly necessary, since plt.hist below will create a figure object

# Create the histogram
plt.hist(trip_miles_series)
plt.title("Distribution of Trip Miles")
plt.xlabel("Trip Miles")
plt.ylabel("Frequency")

plt.show()
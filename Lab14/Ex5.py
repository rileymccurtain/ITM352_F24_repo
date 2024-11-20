# Create a scatter plot of fares and distances
import matplotlib.pyplot as plt
import pandas as pd

# Use different plot styles
#plt.style.use('ggplot')
#plt.style.use("fivethirtyeight")
plt.style.use("dark_background")

trips_df = pd.read_json("../Trips from area 8.json")
trip_miles_gt_0 = trips_df[['trip_miles', 'fare']].query('trip_miles > 2')

fare_series = trip_miles_gt_0.fare 
trip_miles = trip_miles_gt_0.trip_miles

plt.plot(fare_series, trip_miles, marker="o", linestyle="none", alpha=0.3)
plt.title("Fare by Taxi Trip Miles > 2")
plt.xlabel("Fare in $")
plt.ylabel("Distance in Miles")

plt.savefig("FaresXMiles.2.png", dpi=300)
plt.show()
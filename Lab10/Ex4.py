import pandas as pd

# Read a json file of taxi trip data and create a DataFrame from it 

results_df = pd.read_json("Taxi_Trips.json")
print(results_df.describe())
print(results_df.head(10))

print("The median fare value is: ", results_df['fare'].median())
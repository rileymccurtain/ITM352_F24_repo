import pandas as pd
# Read in a CSV file containing real estate data in NYC, and turn it into a DataFrame

df_homes = pd.read_csv("../homes_data.csv")

# Print the dimensions of the data and the first 10 rows
shape = df_homes.shape
print(f"The homes data has {shape[0]} rows and {shape[1]} columns")

# Select properties with 500 or more units and drop unnecessary columns 
df_big_apartments = df_homes[df_homes.units >= 500]
df_big_apartments = df_big_apartments.drop(columns=['id', 'easement'])

# Since some of the data types are incorrect, coerce them to the correct data type 
df_big_apartments['land_sqft'] = pd.to_numeric(df_big_apartments['land_sqft'], errors='coerce')
df_big_apartments['gross_sqft'] = pd.to_numeric(df_big_apartments['gross_sqft'], errors='coerce')
df_big_apartments['sale_price'] = pd.to_numeric(df_big_apartments['sale_price'], errors='coerce')

# Look at the data types 
print(df_big_apartments.info())

# Drop rows with NaN values and drop duplicate rows 
df_big_apartments = df_big_apartments.dropna()
df_big_apartments = df_big_apartments.drop_duplicates(df_big_apartments.columns, keep='first')
df_big_apartments = df_big_apartments[df_big_apartments['sale_price'] > 0]

print("After filtering out 0 sales: \n", df_big_apartments.head(10))
print("The average sales price of big apartments is: $", round(df_big_apartments['sale_price'].mean(),2))
import pandas as pd

# List of individuals' ages
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]


#Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

dict = zip(ages, gender)

#Convert the dictionary to a DataFrame, with names as the keys
df = pd.DataFrame(dict, columns=['Age', 'Gender'], index=names) 

# Print and summarize the DataFrame 
print(df)
summary = df.describe()
print(summary)

# Calculate the average age by gender 
average_age_by_gender = df.groupby('Gender')['Age'].mean()
print(average_age_by_gender) 
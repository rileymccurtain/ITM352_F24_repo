# Create a bar chart of tips by payment type
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

trips_df = pd.read_json("../Trips from area 8.json")

# Grab the tips and payment type columns from the data frame; drop rows with empty values
trips_df = trips_df.dropna()
trips_df = trips_df[['tips', 'payment_type']]
trips_df = trips_df.astype({'tips': float})
trips_df = trips_df.set_index('payment_type')

tips_by_payment_type = trips_df.groupby('payment_type').sum()

x_labels = pd.Series(tips_by_payment_type.index.values)
y_values = pd.Series(tips_by_payment_type['tips'].values)

bars = np.array(range(len(x_labels)))
plt.xticks(bars, x_labels, color='red', fontweight='bold')

plt.bar(bars, y_values)

plt.title("Taxi Tips by Payment Type")
plt.xlabel("Payment Type")
plt.ylabel("Tips in $")
plt.show()
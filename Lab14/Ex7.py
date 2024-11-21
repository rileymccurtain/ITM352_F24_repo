# Create a heatmap of pickup and dropoff areas
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import numpy as np

trips_df = pd.read_csv("taxi trips Fri 7_7_2017.csv")

trips_df = trips_df[['dropoff_community_area', 'pickup_community_area']]
trips_freq = pd.crosstab(trips_df.pickup_community_area, \
                         trips_df.dropoff_community_area).stack().reset_index().rename(columns={0:'numtrips'})

trips_freq = trips_freq.query('numtrips>20')
trips_freq = trips_freq.pivot(index="pickup_community_area",
                columns="dropoff_community_area", 
                values="numtrips")


trips_freq = trips_freq.replace(np.nan, 0)
trips_freq = trips_freq.astype(int)
fig = plt.figure()

ax = sns.heatmap(trips_freq, annot=True, fmt= "d", cmap="YlOrRd")

plt.show()
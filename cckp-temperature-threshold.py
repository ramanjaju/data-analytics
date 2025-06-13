import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('/Users/raman/Downloads/WB_CCKP_HDD65.csv')
print(df.head())
print(df.info())

print(df.nunique())

# Drop columns where all values are the same and create a new filtered DataFrame consisting only of the required columns
filtered_df = df.drop(columns=df.columns[df.nunique() == 1])
print(filtered_df.sample(5))
print(filtered_df.isnull().sum())
#returns no null values hence no need for any more filtering

print(filtered_df.describe(include='all'))

# Choose a few countries of interest
countries = ['India', 'United States', 'Germany', 'Canada']

subset = filtered_df[filtered_df['REF_AREA_LABEL'].isin(countries)]


# for a sample of 4 countries, this plots the average temperature over the years, higher the line, colder the country.
plt.figure(figsize=(10, 6))
sns.lineplot(data=subset, x='TIME_PERIOD', y='OBS_VALUE', hue='REF_AREA_LABEL')
plt.title("HDD65 Over Time")
plt.xlabel("Year")
plt.ylabel("Heating Degree Days (HDD65)")
plt.grid(True)
plt.tight_layout()
plt.show()


#Plotting the distribution of HDD65 values
plt.figure(figsize=(8, 5))
sns.histplot(filtered_df['OBS_VALUE'], bins=50, kde=True)
plt.title("Distribution of HDD65 Values")
plt.xlabel("HDD65")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# arranging by highest OBS_Value to find top 10 cold countries
top_cold = filtered_df.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().sort_values(ascending=False).head(10)


plt.figure(figsize=(10, 5))
sns.barplot(x=top_cold.values, y=top_cold.index, palette='Blues_r')
plt.title("Top 10 Coldest Countries (Highest Average HDD65)")
plt.xlabel("Average HDD65")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

yearly_avg = filtered_df.groupby('TIME_PERIOD')['OBS_VALUE'].mean().reset_index()

#Plotting the linegraph for the global average HDD65 of all the countries over the years from 1950-2022
plt.figure(figsize=(10, 5))
sns.lineplot(data=yearly_avg, x='TIME_PERIOD', y='OBS_VALUE')
plt.title("Global Average HDD65 Over Time")
plt.xlabel("Year")
plt.ylabel("Avg HDD65")
plt.grid(True)
plt.tight_layout()
plt.show()

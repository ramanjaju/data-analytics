import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math

df = pd.read_csv('/Users/raman/Downloads/01352099999.csv')
print(df.head())
# print(df.info())

df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
numeric_cols = ['MAX', 'MIN', 'PRCP', 'SNDP', 'GUST', 'MXSPD']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

placeholders = [999.9, 9999.9, 999.99, 99.99, 9999, 99.9]
for col in numeric_cols:
    for val in placeholders:
        df[col] = df[col].replace(val, np.nan)


def avg_temperature_2024():
    sum = 0
    for temp in df['TEMP']:
        sum = sum + temp
    return sum/len(df['TEMP'])
    
print(avg_temperature_2024())


df['HeavyRain'] = df['PRCP'] > 3

df['Storm'] =  df['GUST'] > 50

df.sort_values('DATE', inplace=True)


df['HotDay'] = df['MAX'] > 50 

# Identify groups of consecutive hot days
df['HeatwaveGroup'] = (df['HotDay'] != df['HotDay'].shift()).cumsum()

# Count consecutive days in each group
heatwave_lengths = df[df['HotDay']].groupby('HeatwaveGroup').size()

# Identify groups with 2 or more consecutive hot days
valid_heatwave_groups = heatwave_lengths[heatwave_lengths >= 2].index

# Mark those as actual heatwave events
df['Heatwave'] = df['HeatwaveGroup'].isin(valid_heatwave_groups)


df['Dry'] = df['PRCP'] < 0.005

# Group consecutive dry days
df['DroughtGroup'] = (df['Dry'] != df['Dry'].shift()).cumsum()
drought_lengths = df[df['Dry']].groupby('DroughtGroup').size()
valid_drought_groups = drought_lengths[drought_lengths >= 20].index

# Mark actual drought days
df['Drought'] = df['DroughtGroup'].isin(valid_drought_groups)

df['Month'] = df['DATE'].dt.to_period('M')
monthly_summary = df.groupby('Month')[['Heatwave', 'Drought', 'HeavyRain', 'Storm']].sum()
print(monthly_summary)

def plot_monthly_summary():
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_summary, markers=True)
    plt.title('Monthly Summary of Weather Events')
    plt.xlabel('Month')
    plt.ylabel('Number of Events')
    plt.xticks(rotation=45)
    plt.legend(title='Event Type')
    plt.tight_layout()
    plt.show()

def plot_heatmap():
    heatmap_data = df.pivot_table(index=df['DATE'].dt.month, columns=df['DATE'].dt.year, values='MAX', aggfunc='mean')
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".1f")
    plt.title('Average Monthly Maximum Temperature Heatmap')
    plt.xlabel('Year')
    plt.ylabel('Month')
    plt.show()

monthly_summary.index = monthly_summary.index.astype(str)
print(monthly_summary.dtypes)
plot_monthly_summary()
plot_heatmap()



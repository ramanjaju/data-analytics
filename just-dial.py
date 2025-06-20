import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
import pandas as pd

# Load original file
file_path = "/Users/raman/Downloads/Just Dial  2023-2024 (1).xlsx"
xls = pd.ExcelFile(file_path)

# Load sheets
df_2023 = xls.parse('2023')
df_2024 = xls.parse('2024')
df_2025 = xls.parse('2025')

#Combine 2024 and 2025
df_24_25 = pd.concat([df_2024, df_2025], ignore_index=True)

print(df_2023.info())
print(df_24_25.info())
df_2023.drop(columns = ['Date.1', 'Date.2', 'Date.3', 'Date.4', '4 Month End Followup', 'Remark 2', 'Remark 3'], inplace=True, errors='ignore')
print(df_2023.columns)


# Total Leads
total_leads = len(df_2023)

# Top 10 Most Popular Courses
top_courses = df_2023['Interested Course'].value_counts().nlargest(10)


# Define mapping for standardizing admission status values
status_mapping = {
    'Intrested': 'Interested',
    'Not intersted': 'Not Interested',
    'Not Intersted': 'Not Interested',
    'Not Interested': 'Not Interested',
    'Not Received the call': 'Not Received the Call',
    'Call Back': 'Call Back',
    'Looking for Job': 'Looking for Job',
    'Enrolled': 'Enrolled',
    'Laptop Store': 'Laptop Store',
    'Placement Agencies': 'Placement Agencies',
    'Join Other Institute': 'Join Other Institute'
}

# Apply the mapping to the DataFrame
df_2023['Admission Status'] = df_2023['Admission Status'].replace(status_mapping)


# Admission Status Distribution
admission_status = df_2023['Admission Status'].value_counts()

# Follow-Up Trends
df_2023['Date'] = pd.to_datetime(df_2023['Date'], errors='coerce')
follow_up_dates = df_2023['Date'].value_counts().nlargest(10)


# Plotting Total Leads
plt.figure(figsize=(8, 2))
plt.title('Total Leads in 2023')
plt.bar(['Total Leads'], [total_leads])
plt.ylabel('Count')
plt.savefig('total_leads_2023.png')
plt.show()

# Plotting Top 10 Most Popular Courses
plt.figure(figsize=(18, 8))
plt.title('Top 10 Most Popular Courses in 2023')
sns.barplot(x=top_courses.values, y=top_courses.index)
plt.xlabel('Count')
plt.savefig('top_courses_2023.png')
plt.show()


# Plotting Admission Status Distribution
plt.figure(figsize=(12, 8))
plt.title('Admission Status Distribution in 2023')
sns.barplot(x=admission_status.values, y=admission_status.index)
plt.xlabel('Count')
plt.savefig('admission_status_2023.png')
plt.show()

# Plotting Top 10 Follow-Up Dates
plt.figure(figsize=(12, 8))
plt.title('Top 10 Follow-Up Dates in 2023')
sns.barplot(x=follow_up_dates.values, y=follow_up_dates.index)
plt.xlabel('Count')
plt.savefig('follow_up_dates_2023.png')
plt.show()

print(df_2023['Admission Status'].value_counts())


# Group by week and count leads
weekly_report = df_2023.resample('W-SUN', on='Date').size()

# Print weekly report
print(weekly_report)

# Plotting weekly report

plt.figure(figsize=(12, 6))
plt.title('Weekly Leads Report for 2023')
plt.plot(weekly_report.index, weekly_report.values, marker='o')
plt.xlabel('Week Ending On')
plt.ylabel('Number of Leads')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('weekly_leads_report_2023.png')
plt.show()

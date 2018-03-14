########## Import packages ##########

# Import numpy/pandas
import numpy as np
import pandas as pd
# Used to create data visualizations
import matplotlib.pyplot as plt
# Used to convert month number to month string
import calendar as cal
# Used to convert seconds into formatted time
import time




########## Import data ##########

# Import data from each Chicago, New York City, and Washington DC
chi = pd.read_csv('chicago.csv')
ny = pd.read_csv('new_york_city.csv')
dc = pd.read_csv('washington.csv')




########## Modify Data ##########

# Add column for city in ny, chi, dc
chi['City Name'] = 'chi'
ny['City Name'] = 'ny'
dc['City Name'] = 'dc'

# Combine ny, chi, dc into one dataset
all_data = pd.concat([chi, ny, dc])

# Turn 'Start Time' and 'End Time' columns into datetimes.
all_data['Start Time'] = pd.to_datetime(all_data['Start Time'])
all_data['End Time'] = pd.to_datetime(all_data['End Time'])

# Add columns for month, day of week, and hour of day
all_data['Start Month'] = (all_data['Start Time']).dt.month
all_data['Start DOW'] = (all_data['Start Time']).dt.weekday_name
all_data['Start HOD'] = (all_data['Start Time']).dt.hour




########## Data Inquiry ##########

#### Function for obtaining data based on inputs ####
def data_inquiry(city, month=None, dow=None):
	'''
	Funtion that obtains data based on user inputs
	Inputs: City, and month or dow
	Outputs: Motivate bike data for those inputs
	'''
	data = all_data
	if city:
		data = all_data.loc[all_data['City Name'] == city]
	if month:
		data = data.loc[data['Start Month'] == int(month)]
	elif dow:
		data = data.loc[data['Start DOW'] == dow]
	return data.to_json




########## Data Summary ##########


#### Helper functions for counting values in a DataFrame column ####
# groups data based on a column
def group_data(data, column_name):
	return data.groupby(column_name)

# finds the group with the most values
def max_group(group_data):
	return group_data.size().idxmax()

# counts the number of records
# given grouped data and a value
def count_values(grouped_data, group_value):
	return len(grouped_data.groups[group_value])

# finds group with the most records
def find_max_group(data, column_name):
	# group data by column_name
	grouped_data = group_data(data, column_name)
	# return group with most values
	return max_group(grouped_data)


#### Q1: What is the most popular month for start time? ####

# 'Start Month' with most records
max_start_month = find_max_group(all_data, 'Start Month')
# Convert month int to month string
max_start_month = cal.month_name[max_start_month]


#### Q2: What is the most popular day of week for start time? ####

# 'Start DOW' with most records
max_start_dow = find_max_group(all_data, 'Start DOW')


#### Q3: What is the most popular hour of day for start time? ####

# Formats the hour integer into a string
def format_hour(time_int):
	'''
	Converts the hour of the day in integer format
	To the hour of the day in string format
	'''
	if time_int == 0:
		time_str = "12:00 AM"
	elif time_int < 12:
		time_str = "%s:00 AM" % time_int
	else:
		time_str = "%s:00 PM" % time_int
	return time_str

# 'Start HOD' with most records
max_start_hod = find_max_group(all_data, 'Start HOD')
# Format HOD
max_start_hod = format_hour(max_start_hod)


#### Q4: What is the total trip duration and average trip duration? ####

def format_seconds(sec):
	'''
	Formats seconds into an array of
	[years, months, weeks, days, hours, minutes, seconds]
	'''
	# Seconds in a minute, hour, day, week, month, year
	sec_min, sec_hour, sec_day, sec_week, sec_month, sec_year = (60, 3600, 86400, 604800, 2628000, 31536000)
	formatted_date = ''
	# Format seconds to year, week, day, hour, minute
	# Years
	years = int(sec // sec_year)
	sec_left = sec % sec_year
	# Months
	months = int(sec_left // sec_month)
	sec_left = sec_left % sec_month
	# Weeks
	weeks = int(sec_left // sec_week)
	sec_left = sec_left % sec_week
	# Days
	days = int(sec_left // sec_day)
	sec_left = sec_left % sec_day
	# Hours
	hours = int(sec_left // sec_hour)
	sec_left = sec_left % sec_hour
	# Minutes
	minutes = int(sec_left // sec_min)
	seconds = int(round(sec_left % sec_min))
	# Array of years, months, weeks, days, hours, minutes, seconds
	time_array = [years, months, weeks, days, hours, minutes, seconds]
	return time_array


def time_to_string(time_array):
	'''
	Converts an array of [years, months, weeks, days, hours, minutes, seconds]
	into a string describing those values
	'''
	years, months, weeks, days, hours, minutes, seconds = time_array
	years_str, months_str, weeks_str, days_str, hours_str, minutes_str, seconds_str = ("", "", "", "", "", "", "")
	if years != 0:
		years_str = "%s Years, " % years
	if months != 0:
		months_str = "%s Months, " % months
	if weeks != 0:
		weeks_str = "%s Weeks, " % weeks
	if days != 0:
		days_str = "%s Days, " % days
	if hours != 0:
		hours_str = "%s Hours, " % hours
	if minutes != 0:
		minutes_str = "%s Minutes, and " % minutes
	seconds_str = "%s Seconds." % seconds
	output_str = years_str + months_str + weeks_str + days_str + hours_str + minutes_str + seconds_str
	return output_str

# total trip duration
total_trip_duration = time_to_string(format_seconds(all_data['Trip Duration'].sum()))

# average trip duration
avg_trip_duration = time_to_string(format_seconds(all_data['Trip Duration'].mean()))

#### Q5: What is the most popular start station and most popular end station? ####

# 'Start Station' with most records
max_start_station = find_max_group(all_data, 'Start Station')

# 'End Station' with most records
max_end_station = find_max_group(all_data, 'End Station')


#### Q6: What is the most popular trip? ####

# 'Start Station' and 'End Station' with most records
max_start_end_station = find_max_group(all_data, ['Start Station', 'End Station'])


#### Q7: What are the counts of each user type? ####

# Group all data by user type
group_user_type = group_data(all_data, 'User Type')
customers = count_values(group_user_type, 'Customer')
subscribers = count_values(group_user_type, 'Subscriber')


#### Q8: What are the counts of gender? ####

# Group all_data by gender
group_gender = group_data(all_data, 'Gender')
# Number of males/females
males = count_values(group_gender, 'Male')
females = count_values(group_gender, 'Female')


#### Q9: What are the earliest (oldest person), most recent (youngest person), and most popular birth years?

# earliest (oldest person)
by_oldest = all_data['Birth Year'].min()
# most recent (youngest person)
by_youngest = all_data['Birth Year'].max()

# most popular birth years
# group data by birth year
by_group = all_data.groupby('Birth Year')
# count number of records for each birth year, sort descending
by_count = by_group.size().sort_values(ascending=False)
# obtain the top 3 most common birth years
by_popular = tuple(by_count.index[0:3])
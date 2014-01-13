# Find the average speeds and flows for each station during rush hour

import pandas as pd
import loadfreewaydata
import datetime

business_days = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 22, 23, 24, 25, 28, 29, 30, 31]
night_rush_hour = [17, 18]

rawdata = loadfreewaydata.load_measurement_data_hour('../d07_text_station_hour_2013_01.txt')
rawdata['day'] = map(lambda x : x.astype(datetime.datetime).day, rawdata['timestamp'])
rawdata['hour'] = map(lambda x : x.astype(datetime.datetime).hour, rawdata['timestamp'])

# filter out non-workdays
filtered = rawdata[rawdata['day'].isin(business_days)]
# filter out non-rush hour times
filtered = filtered[filtered['hour'].isin(night_rush_hour)]

# use groupby to find averages
filtered[['station', 'avgspeed', 'totalflow']].groupby('station').mean()



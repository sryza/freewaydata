import pandas as pd
import numpy as np
import loadfreewaydata
import traveltime
import matplotlib.pyplot as plt
import datetime

rawdata = loadfreewaydata.load_measurement_data_5min('../d07_text_station_5min_2013_03_06.txt')
bystation = {g[0]:g[1] for g in rawdata.groupby('station')}

freeway_metadata = loadfreewaydata.load_freeway_metadata('../d07_stations_2012_09_06.txt')

fwy = (405, 'S')
start_station = 718287
end_station = 718300
path = freeway_metadata[fwy].loc[start_station:end_station].index
# filter out stations with no speed observations
path = [station for station in path if bystation[station]['avgspeed'].count() > 0]
print "path: " + str(path)

five_mins = hour = np.timedelta64(1000000 * 60 * 5)
start_times = [np.datetime64('2013-03-06 08:00:00')]
for i in range(36):
  start_times.append(start_times[-1] + five_mins)

#start_times = [np.datetime64('2013-03-06 08:{:0>2}:00'.format(i * 5)) for i in range(6)]
print start_times
travel_times = map(lambda x : traveltime.travel_time(x, path, bystation, freeway_metadata[fwy], time_granularity = 60 * 5)[1], start_times)

plt.plot_date(map(lambda x : x.astype(datetime.datetime), start_times), travel_times, '-')


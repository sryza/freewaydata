import pandas as pd
import matplotlib.pyplot as plot
import pylab
import plotonmap
from sklearn.cluster import KMeans

map_template_path = 'html/showfreeways.html.template'
pylab.show()
pylab.ion()

# load stuff
colnames = ['timestamp', 'station', 'district', 'route', 'direction', 'lanetype', 'stationlen', 'samples', 'percentobserved', 'totalflow', 'avgoccupancy', 'avgspeed', 'delay35', 'delay40', 'delay45', 'delay50', 'delay55', 'delay60']
for i in range(1,9):
  colnames.extend(['laneflow' + str(i), 'laneavgoccupancy' + str(i), 'laneavgspeed' + str(i)])

rawdata = pd.read_csv('d07_text_station_hour_2013_01.txt', header=None, names=colnames, parse_dates=[0])

station_data = plotonmap.load_station_data('d07_stations_2012_09_06.txt')

bystation = rawdata.groupby('station')

# plot a station across time:
# rawdata[rawdata['station'] == 715933]['avgspeed'].plot()


# TODO: find out which station has the max and min avg speed

# TODO: how many stations report on multiple lanes. make a histogram of of number of lanes.

# find out correlation between speed and flow for each station.  do a scatterplot of this correlation by station.
station_corrs = {}
for group in bystation:
  stationdata = group[1]
  corr = stationdata[['avgspeed', 'totalflow']].corr()
  station_corrs[group[0]] = corr['totalflow']['avgspeed']

#plot.hist(station_corrs.values(), bins=20, range=(-1, 1))

# plot on map
for (sid, corr) in station_corrs.iteritems():
  station_corrs[sid] = (corr + 1.0) / 2.0

plotonmap.plot_on_map(station_corrs, station_data, map_template_path, 'stationcorrs.html')

# TODO: cluster stations by correlations and plot clusters
# kmeans = KMeans(init='k-means++', n_clusters=5, n_init=10)
# kmeans.fit(corrs) # TODO

# get time sequences


# plot distribution of 


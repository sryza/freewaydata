import pandas as pd
import loadfreewaydata
import sklearn.cluster as cluster
import plotonmap
import numpy as np

#rawdata = loadfreewaydata.load_measurement_data_hour('../d07_text_station_hour_2013_01.txt')
freeway_data = loadfreewaydata.load_freeway_metadata('../d07_stations_2012_09_06.txt')

def cluster_stations(rawdata, colname, filename):
  times = rawdata['timestamp'].unique()
  
  speeds_by_station = {g[0]:g[1][colname] for g in rawdata.groupby('station')}
  for station_speeds in speeds_by_station.values():
    station_speeds.index = times
  
  # rows are stations, columns are times
  station_mat = pd.DataFrame(data=speeds_by_station).transpose()
  
  # filter out stations with no data
  station_mat = station_mat[station_mat.count(axis=1) == 744] # TODO: replace 744 with num columns
  
  # do the clustering
  num_clusters = 5
  kmeans = cluster.KMeans(n_clusters = num_clusters)
  kmeans.fit(station_mat)
  
  colors = np.linspace(0, 1, num_clusters)
  station_colors = {station_mat.index[i]:colors[kmeans.labels_[i]] for i in range(len(station_mat.index))}
  
  plotonmap.plot_on_map(station_colors, freeway_data, '../html/showfreeways.html.template', filename)

# cluster_stations(rawdata, 'avgspeed', '../speedclusters.html')
# cluster_stations(rawdata, 'totalflow', '../flowclusters.html')


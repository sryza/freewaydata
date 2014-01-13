import pandas as pd

def load_measurement_data_hour(measurements_file):
  col_names = ['timestamp', 'station', 'district', 'route', 'direction', 'lanetype', 'stationlen', 'samples', 'percentobserved', 'totalflow', 'avgoccupancy', 'avgspeed', 'delay35', 'delay40', 'delay45', 'delay50', 'delay55', 'delay60']
  for i in range(1, 9):
    col_names.extend(['laneflow' + str(i), 'laneavgoccupancy' + str(i), 'laneavgspeed' + str(i)])

  return pd.read_csv(measurements_file, header=None, names=col_names, parse_dates=[0])

def load_measurement_data_5min(measurements_file):
  col_names = ['timestamp', 'station', 'district', 'route', 'direction', 'lanetype', 'stationlen', 'samples', 'percentobserved', 'totalflow', 'avgoccupancy', 'avgspeed']
  for i in range(1, 9):
    col_names.extend(['lanesamples' + str(i), 'laneflow' + str(i), 'laneavgoccupancy' + str(i), 'laneavgspeed' + str(i), 'laneobserved' + str(i)])

  return pd.read_csv(measurements_file, header=None, names=col_names, parse_dates=[0])

"""
Loads a dict of freeway ID to dataframe with station IDs on that freeway.
Sorted by postmile.
"""
def load_freeway_metadata(stations_file):
  station_data = pd.read_csv(stations_file, sep='\t', index_col=0)
  by_fwy_dir = station_data.groupby(['Fwy', 'Dir'])
  fwys = {}
  for group in by_fwy_dir:
    fwys[group[0]] = group[1].sort('Abs_PM')
  
  return fwys


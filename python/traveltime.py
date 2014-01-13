import numpy as np
import pandas as pd

def datetime64_to_microseconds(dt):
  return dt.astype('uint64')

def travel_time(start_time, path, measurements_by_station, station_metadata, time_granularity=60*60):
  """Calculate the travel time along the given path at the given start time
  
  Args:
  path - list of station IDs that must be traversed to reach the destination
  start_time - start time datetime64
  station_data - dataframes grouped by station
  time_granularity - granularity of samples in seconds
  """
  time_granularity *= 1000000 # convert to microseconds
  time = datetime64_to_microseconds(start_time)
  total_dist = 0
  
  for i in range(len(path)-1):
    # calculate how long it takes to get to the next station based on the
    # current time
    sid1 = path[i]
    sid2 = path[i+1]
    
    measurements = measurements_by_station[sid1]
    quantized = np.datetime64(time - time % time_granularity)
    filtered = measurements[measurements['timestamp'] == quantized]
    speed = filtered.iloc[0]['avgspeed']
    if np.isnan(speed):
      return (np.nan, np.nan)
    
    station1_metadata = station_metadata.loc[sid1]
    station2_metadata = station_metadata.loc[sid2]
    dist = abs(station1_metadata['Abs_PM'] - station2_metadata['Abs_PM'])
    total_dist += dist
    
    # TODO: what if speed is NAN? interpolate
    time += 1000000 * 60 * 60 * dist / speed

  return (total_dist, np.datetime64(time) - start_time)

def test_travel_time():
  path = [213, 224, 285, 485]
  station_metadata = pd.DataFrame({'Abs_PM' : pd.Series([0, 60, 75, 85], index=[213, 224, 285, 485])})
  base_time = np.datetime64('2013-01-01')
  hour = np.timedelta64(1000000 * 60 * 60)
  times = pd.Series([base_time, base_time + hour], index=range(2))
  speeds = [[40, np.nan], [np.nan, 60], [np.nan, 120], [np.nan, np.nan]]
  samples_by_station = {path[i] : pd.DataFrame({'timestamp' : times, 'avgspeed' : speeds[i]}) for i in range(len(path))}
  start_time = base_time + np.timedelta64(5 * 1000000 * 60) # start at 5 minutes past the hour

  # Traveling 60 miles at 40 MPH should put us in the next hour (total time = 1:35)
  # Then traveling 15 miles at 60 MPH should keep us in the same hour (total time = 1:50)
  # Then 10 miles at 120 MPH should get us to our destination (total time = 1:55)
  # Travel time is 1:55 minus the 5 minutes past the hour we started at, so 1:50
  print travel_time(start_time, path, samples_by_station, station_metadata)

if __name__ == '__main__':
  test_travel_time()

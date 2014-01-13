import json
import pandas as pd
import heatcolors

STRING_TO_REPLACE = "FWYS_GO_HERE"

"""
station_colors maps station ids to the [0.0,1.0] heats they should be displayed in
"""
def plot_on_map(station_heats, station_data, template_path, out_path, include_fwys=None):
  fwys = {}
  for (fwyid, fwy_station_data) in station_data.iteritems():
    points = []
    strfwyid = str(fwyid[0]) + str(fwyid[1])
    print strfwyid
    if include_fwys is not None and strfwyid not in include_fwys:
      continue
    for station_id, row in fwy_station_data.iterrows():
      if station_id in station_heats:
        heat = station_heats[station_id]
        color = 0.0 if pd.isnull(heat) else heatcolors.gradient(heat)
        points.append((row['Latitude'], row['Longitude'], color))

    fwys[strfwyid] = points

  write_out_html_file(template_path, out_path, json.dumps(fwys))

def write_out_html_file(template_path, out_path, fwy_str):
  template_file = open(template_path)
  template_str = template_file.read()
  replace_index = template_str.find(STRING_TO_REPLACE)
  before_str = template_str[0:replace_index]
  after_str = template_str[replace_index + len(STRING_TO_REPLACE):]
  
  out_file = open(out_path, 'w')
  out_file.write(before_str)
  out_file.write(fwy_str)
  out_file.write(after_str)
  out_file.close()


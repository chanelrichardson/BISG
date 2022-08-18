import pandas as pd
import os
import tqdm
import geopandas as gpd 
my_encoding = 'ISO-8859-1'
for year in ["20"]:
  #p = pd.read_csv(f"voterfile_{year}.csv", low_memory=False, dtype={"GEOID20":str})
  df = pd.read_csv('VM2Uniform--TX--2021-03-25.tab', encoding=my_encoding, low_memory=False, sep='\t', iterator=True, chunksize=1000)
  p = pd.concat(df, ignore_index=True)
  for col in p.columns: print(col)
  os.makedirs(f"county-chunks20", exist_ok=True)
  for county in tqdm.tqdm(p.County.unique()): 
    p_mini = p[p.County == county]
    if " " in county:
      county_new = county.split(" ")[0]
      county_new2 = county.split (" ")[-1].capitalize()
      county = county_new + county_new2
    f_name = f"{county.capitalize()}-header20-party.csv"
    p_mini.to_csv(f"county-chunks20/{f_name}", index=False)


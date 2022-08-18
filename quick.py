import geopandas as gpd
import pandas as pd
import json
"""
data_dict = {"STATE_2010":str, 
             "COUNTY_2010":str, 
             "TRACT_2010":str, 
             "BLK_2010":str, 
             "STATE_2020":str, 
             "COUNTY_2020":str, 
             "TRACT_2020": str, 
             "BLK_2020":str}
tx = pd.read_csv("tab2010_tab2020_st48_tx.txt", sep="|", dtype=data_dict)
tx.STATE_2010 = tx.STATE_2010.astype(str)
tx = tx[tx.STATE_2010 == '48']

tx["GEOID10"] = tx.STATE_2010 + tx.COUNTY_2010 + tx.TRACT_2010 + tx.BLK_2010
tx["GEOID20"] = tx.STATE_2020 + tx.COUNTY_2020 + tx.TRACT_2020 + tx.BLK_2020

tx_dict = tx.set_index("GEOID10").to_dict()["GEOID20"]

with open("tx_tabblock_10_20.json", "w+") as f:
  json.dump(tx_dict, f)
"""
mapping = json.load(open("tx_tabblock_10_20.json"))

tx = pd.read_csv("tx_pop_vap.csv", dtype={"GEOID20":str})
for year in ["16", "18", "20"]: 
  vf = pd.read_csv(f"voterfile_{year}.csv", dtype={"GEOID20":str}, low_memory=False).rename(columns={"GEOID20":"GEOID10"})
  vf["GEOID20"] = vf["GEOID10"].map(mapping)
  print(f"vf before: {len(vf)}")
  vf = vf[vf.GEOID20.isin(tx.GEOID20)]
  print(f"vf after: {len(vf)}")
  vf.to_csv(f"voterfile_{year}.csv", index=False)

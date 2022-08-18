import glob
import pandas as pd

headers = glob.glob("county-chunks18-archive/*header18.csv")
runoff = 0
primary = 0
gen = 0
for header in headers:
  h = pd.read_csv(header)
  c_name = header.split("/")[-1].split("-header")[0]
  #vp = pd.read_csv(f"county-chunks18-archive/{c_name}-voter-pred.csv")[["LALVOTERID", "Runoff_2020_07_14"]]
  hp = pd.read_csv(f"county-chunks18/{c_name}-header18-party.csv")[["LALVOTERID", "PRI_BLT_2018"]]
  #h = h.merge(vp, on = "LALVOTERID")
  h = h.merge(hp, on = "LALVOTERID")
  runoff += len(h[(h.PRI_BLT_2018 == "D") & (h.Runoff_2018_05_22 == "Y")])
  primary += len(h[(h.PRI_BLT_2018 == "D") & (h.Primary_2018_03_06 == "Y")])
  gen += len(h[(h.PRI_BLT_2018 == "D") & (h.General_2018_11_06 == "Y")])

print(f"General: {gen}, Primary: {primary}, Runoff: {runoff}")

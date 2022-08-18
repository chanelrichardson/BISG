import glob
import pandas as pd

my_fs = glob.glob("county-chunks18/*party*")

my_elecs = ["General_2018_11_06", "Runoff_2018_05_22", "Primary_2018_03_06"]
for elec in my_elecs:
  tot_sum = 0
  for file in my_fs: 
    f = pd.read_csv(file)
    c_name = file.split("/")[-1].split("-header")[0]
    corr = pd.read_csv(f"county-chunks18/{c_name}-header18-corrected.csv")[["LALVOTERID", elec]]
    f = f.merge(corr, on = "LALVOTERID")
    tot_sum += len(f[(f[elec] == "Y") & (f.PRI_BLT_2018 == "D")])
  print(elec, tot_sum) 


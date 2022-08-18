import pandas as pd
import glob

my_fs = glob.glob("county-chunks20/*header20-corrected.csv")
#f = pd.read_csv(my_fs[0])
for i, fle in enumerate(my_fs[40:]):
  c_name = fle.split("/")[-1].split("-header")[0]
  header = pd.read_csv(f"county-chunks20/{c_name}-voter-pred.csv")[["LALVOTERID", "Runoff_2020_07_14"]]
  #if "Briscoe" in fle:
  f = pd.read_csv(fle)
  if "Runoff_2020_07_14" not in f.columns:
    new_f = f.merge(header, on = "LALVOTERID", how="left")
    print(len(f), len(new_f), f.columns)  
    assert len(f) == len(new_f)
    new_f.to_csv(fle)
    print("Added to", end = " ")
  print(c_name, f"{i}, done")

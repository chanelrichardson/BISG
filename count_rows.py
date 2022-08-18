import glob
import pandas as pd

my_fs = glob.glob("county-chunks20/*voter-pred.csv")
tot_rows = 0
for f in my_fs: 
  file = pd.read_csv(f)
  tot_rows += len(file)
print(tot_rows)

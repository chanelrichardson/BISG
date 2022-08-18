import glob
import pandas as pd
from tqdm import tqdm
year = "20"
year_dict = {"16": ["General_2016-11-08", "Runoff_2016-05-24", "Primary_2016-03-01"],
             "18": ["General_2018_11_06", "Runoff_2018_05_22", "Primary_2018_03_06"],
             "20": ['General_2020_11_03', 'Primary_2020_03_03', 'Runoff_2020_07_14']}
my_files = glob.glob(f"county-chunks{year}/*header*corrected*.csv")
my_election_cols = year_dict[year]
general_col = [col for col in my_election_cols if "General" in col][0]
primary_col = [col for col in my_election_cols if "Primary" in col][0]
runoff_col = [col for col in my_election_cols if "Runoff" in col][0]
print(general_col, primary_col, runoff_col)
 
tot_gen = 0
tot_prim = 0
tot_runoff = 0
for file in tqdm(my_files):
  f = pd.read_csv(file, low_memory=False)
  if general_col in f.columns:
    tot_gen += len(f[f[general_col] == "Y"])
    tot_prim += len(f[f[primary_col] == "Y"])
    tot_runoff += len(f[f[runoff_col] == "Y"])
  print(tot_gen, tot_prim, tot_runoff)    
print(f"General: {tot_gen}, Primary: {tot_prim}, Runoff: {tot_runoff}")


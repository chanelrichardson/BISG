import glob
import pandas as pd

surnames = pd.read_csv("All-Surname-probs.csv")
  
for year in ["16", "18", "20"]:
  my_files = glob.glob(f"county-chunks{year}/*header*corrected.csv")
  new_df = pd.DataFrame(columns=["unique_ln", "all_ln", "unique_ln_in_file", "all_ln_in_file"])
  for i, file in enumerate(my_files): 
    f = pd.read_csv(file)
    f.Voters_LastName = f.Voters_LastName.str.upper()
    new_row = [len(f.Voters_LastName.unique()), len(f.Voters_LastName), len(f.Voters_LastName[f.Voters_LastName.isin(surnames.NAME)].unique()), len(f.Voters_LastName[f.Voters_LastName.isin(surnames.NAME)])]
    new_df.loc[i] = new_row
  
  new_df.to_csv(f"PresentLastNames{year}.csv", index=False)

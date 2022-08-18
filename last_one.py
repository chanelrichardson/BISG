import pandas as pd
import glob
from tqdm import tqdm 
preds = glob.glob("county-chunks20/*voter-pred.csv")
tot_people = 0
tot_zero_rows = 0
surname_probs = pd.read_csv("All-Surname-probs.csv")
tot_def_rows = 0
new_df = pd.DataFrame(columns=["County", "num_voters", "num_voters_in_zero_block", "num_voters_with_default_probs"])
for i, pred in tqdm(enumerate(preds)):
  p = pd.read_csv(pred)
  p.LASTNAME = p.LASTNAME.str.upper()
  p_name = pred.split("/")[-1].split("-voter")[0]
  tot_last_names = len(p)
  tot_present_last_names = len(p[p.LASTNAME.isin(surname_probs.NAME)])
  tot_people += len(p)
  zero_rows = len(p[(p.BLACK_prob == 0) & (p.HISP_prob == 0) & (p.ASIAN_prob == 0) & (p.WHITE_prob == 0) & (p.OTH_prob == 0)])
  def_rows = len(p[(p.BLACK_prob == 0.2) & (p.HISP_prob == 0.2) & (p.ASIAN_prob == 0.2) & (p.WHITE_prob == 0.2) & (p.OTH_prob == 0.2)])
  tot_zero_rows += zero_rows
  tot_def_rows += def_rows
  new_row = [p_name, len(p), zero_rows, def_rows]
  new_df.loc[i] = new_row

  #new_row = [p_name, tot_last_names, tot_present_last_names]
  #new_df.loc[i] = new_row
new_df.to_csv("Pred20Missing.csv", index=False)
print(tot_zero_rows)

import pandas as pd
import argparse
import os
import tqdm
import math
import numpy as np

parser = argparse.ArgumentParser(description="BISG", 
                                 prog="BISG.py")
parser.add_argument("-county", metavar="county", type=str,
                    help="Which county to BISG?")
parser.add_argument("-year", metavar="year", type=str,
                    help="Voter File Year")
args = parser.parse_args()

year = args.year
county = args.county
county_file = f"chunks{year}/{county.capitalize()}-header{year}-corrected.csv"

to_bisg = pd.read_csv(county_file, dtype={"GEOID20-corrected":str, "GEOID20":str}, low_memory=False)
race_prob_df = pd.read_csv("TX-block-race-prob.csv", dtype={"GEOID20":str})
pred_df = pd.read_csv("All-Surname-probs.csv")
county_avg = pd.read_csv("TX-county-race-avg.csv").rename(columns={"OTHER_share":"OTH_share"})

def BISG(row, race_prob_df, pred_df, county_avg):
  last_name = row["Voters_LastName"]
  geoid = row["GEOID20-corrected"]
  county_prob = county_avg[county_avg.COUNTY == county]
  block_prob = race_prob_df[race_prob_df.GEOID20 == geoid]
  if last_name.upper() in list(pred_df.NAME):
    surname_prob = pred_df[["BLACK", "HISP", "ASIAN","WHITE", "OTH"]][pred_df.NAME == last_name.upper()]
    voter_dict = {}
    for race_col in surname_prob.columns:
      if len(block_prob[f"{race_col}_prob"].values) > 0:
        voter_dict[race_col] = (float(surname_prob[race_col].values[0]) * float(block_prob[f"{race_col}_prob"].values[0]))
      else:
        voter_dict[race_col] = county_avg[f"{race_col}_share"][county_avg.COUNTY == county].values[0]
      
    denom = sum(voter_dict.values())
    if denom > 0:
      voter_dict = {k: v/denom for k, v in voter_dict.items()}
      
      new_row = [row.LALVOTERID, last_name, geoid, voter_dict["BLACK"], voter_dict["HISP"], voter_dict["ASIAN"], voter_dict["WHITE"], voter_dict["OTH"]] 
    else:
      black_prob = np.mean(pred_df["BLACK"][pred_df.NAME == last_name.upper()].values)
      hisp_prob = np.mean(pred_df["HISP"][pred_df.NAME == last_name.upper()].values)
      asian_prob = np.mean(pred_df["ASIAN"][pred_df.NAME == last_name.upper()].values)
      white_prob = np.mean(pred_df["WHITE"][pred_df.NAME == last_name.upper()].values)
      oth_prob = np.mean(pred_df["OTH"][pred_df.NAME == last_name.upper()].values)
      new_row = [row.LALVOTERID, last_name, geoid, black_prob, hisp_prob, asian_prob, white_prob, oth_prob]
      print(new_row)        
  elif last_name.upper() not in pred_df.NAME:
    new_row = [row.LALVOTERID, last_name, geoid, county_prob["BLACK_share"].values[0], county_prob["HISP_share"].values[0], county_prob["ASIAN_share"].values[0], county_prob["WHITE_share"].values[0], county_prob["OTH_share"].values[0]]
  if not math.isclose(sum(new_row[3:]), 1, abs_tol=0.01):
    new_row = [row.LALVOTERID, last_name, geoid, county_prob["BLACK_share"].values[0], county_prob["HISP_share"].values[0], county_prob["ASIAN_share"].values[0], county_prob["WHITE_share"].values[0], county_prob["OTH_share"].values[0]]
  assert math.isclose(sum(new_row[3:]), 1, abs_tol=0.01)
  return pd.Series(new_row)

new_df = to_bisg.apply(lambda row: BISG(row, race_prob_df, pred_df, county_avg), axis=1)
assert len(new_df) == len(to_bisg)
new_df = new_df.rename(columns={0: "LALVOTERID", 1: "LASTNAME", 2: "GEOID20", 3: "BLACK_prob", 4:"HISP_prob", 5:"ASIAN_prob", 6:"WHITE_prob", 7:"OTH_prob"})

new_df.to_csv(f"chunks{year}/{county.capitalize()}-voter-pred-corrected.csv", index=False)

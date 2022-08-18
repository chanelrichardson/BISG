import glob
import pandas as pd
import json
import argparse
from tqdm import tqdm 

parser = argparse.ArgumentParser(description="REMERGE", 
                                 prog="remerge.py")
parser.add_argument("-county", metavar="county", type=str,
                    help="Which county to remerge?")
parser.add_argument("-year", metavar="year", type=str,
                    help="Voter File Year")
args = parser.parse_args()

county = args.county
my_year = args.year
year_dict = {"16": ["General_2016-11-08", "Runoff_2016-05-24", "Primary_2016-03-01"],
             "18": ["General_2018_11_06", "Runoff_2018_05_22", "Primary_2018_03_06"], 
             "20": ['General_2020_11_03', 'Primary_2020_03_03', 'Runoff_2020_07_14']}
pri_dict = {"16":"DEM_PRI_BLT_2016-03-01", 
            "18": "PRI_BLT_2018", 
            "20": "PRI_BLT_2020"}
mapping = json.load(open("../tx_blocks_to_vtds.json"))
inverse = {}
for vtd in mapping.keys():
  blocks = mapping[vtd]
  for block in blocks:
    inverse[block] = vtd
pred = f"chunks{my_year}/{county}-voter-pred-corrected.csv"
county_name = pred.split("/")[-1].split("-voter")[0]
header = pd.read_csv(f"chunks{my_year}/{county_name}-header{my_year}-corrected.csv", dtype={"LALVOTERID":str, "GEOID20-corrected":str})

corr = pd.read_csv(f"county-chunks{my_year}/{county_name}-header{my_year}-party.csv", dtype={"LALVOTERID":str}, low_memory=False)[["LALVOTERID", pri_dict[my_year]]]
header = header[["LALVOTERID", "GEOID20-corrected"] + year_dict[my_year]]
header = header.merge(corr, on = "LALVOTERID")
header = header.replace({"Y":1, "D":int(1), "R":int(0), "O":int(0)})
for col in year_dict[my_year] + [pri_dict[my_year]]:
   header[col] = header[col].fillna(int(0))

header[pri_dict[my_year]] = header[pri_dict[my_year]].astype(int)
pred_df = pd.read_csv(pred, dtype={"LALVOTERID":str, "GEOID20":str}, low_memory=False)
pred_df.GEOID20 = pred_df.GEOID20.astype(str)
pred_df = pred_df.merge(header, on = "LALVOTERID")
geoids = []
pred_df["GEOID20-corrected"] = pred_df["GEOID20-corrected"].astype(str)
for ix, row in tqdm(pred_df.iterrows()):
  if "." in row['GEOID20-corrected']:
    new_geoid = row['GEOID20-corrected'].split(".")[0]
    geoids.append(new_geoid)
  else:
    geoids.append(row['GEOID20-corrected'])
pred_df["GEOID20"] = geoids

print(pred_df.head())
cols_to_keep = []
for col in year_dict[my_year]:
  for race in ["BLACK", "HISP", "WHITE", "ASIAN", "OTH"]:
    if "Primary" in col or "Runoff" in col:
      pred_df[f"{race}_{col}"] = pred_df[f"{race}_prob"] * pred_df[col] * pred_df[pri_dict[my_year]]
    else:
      pred_df[f"{race}_{col}"] = pred_df[f"{race}_prob"] * pred_df[col]
    cols_to_keep.append(f"{race}_{col}")
cols_to_keep.append("GEOID20")
if "GEOID20" not in pred_df.columns:
  print(f"{county_name}")
pred_df = pred_df[cols_to_keep]
pred_df.GEOID20 = pred_df.GEOID20.astype(str)
print(type(pred_df.GEOID20[0]))  
pred_df["VTD"] = pred_df["GEOID20"].map(inverse)
print(pred_df["VTD"])
pred_df_mini = pred_df.drop(columns=["GEOID20"])
pred_df_vtd = pred_df.groupby(by="VTD").sum().reset_index()
new_f_name = pred.split(".csv")[0] + "-vtd.csv"
pred_df_vtd.to_csv(new_f_name, index=False)


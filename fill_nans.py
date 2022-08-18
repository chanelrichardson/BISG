import pandas as pd
import glob
from tqdm import tqdm
import argparse
parser = argparse.ArgumentParser(description="FILL_NANS", 
                                 prog="fill_nans.py")
parser.add_argument("-county", metavar="county", type=str,
                    help="Which county to fill?")
parser.add_argument("-year", metavar="year", type=str,
                    help="Voter File Year")
args = parser.parse_args()

year = args.year
county = args.county
county_avg = pd.read_csv("TX-county-race-avg.csv").rename(columns={"OTHER_share":"OTH_share"})

file = f"county-chunks{year}/{county}-voter-pred-corrected.csv"
#print(file) 
f = pd.read_csv(file)
c_name = file.split("/")[-1].split("-voter")[0]
print(c_name)
county_dict = {}
for ix, row in f.iterrows():
  tot_sum = row.BLACK_prob + row.HISP_prob + row.ASIAN_prob + row.WHITE_prob + row.OTH_prob
  if tot_sum == 0:
    for race in ["BLACK", "HISP", "ASIAN", "WHITE", "OTH"]:
      county_dict[race] = county_avg[f"{race}_share"][county_avg.COUNTY == c_name].values[0]
      f[f"{race}_prob"].loc[ix] = float(county_dict[race])
  print(f.head())
#f.to_csv(file, index=False)

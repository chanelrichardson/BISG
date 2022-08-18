import pandas as pd

my_file = "VoterPred16-v4.csv"

vf = pd.read_csv(my_file)

for col in vf.columns:
  if any(c in col for c in ["BLACK", "WHITE", "HISP", "ASIAN"]):
    if "WHITE" in col:
      oth_col = "OTH" + col.split("WHITE")[-1]
      print("OTHER", sum(vf[col]) + sum(vf[oth_col]))
    else:
      print(col, sum(vf[col]))

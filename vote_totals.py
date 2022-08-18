import pandas as pd

vf = pd.read_csv("voterfile_20.csv", low_memory=False)
#vf = pd.read_csv("VM2--TX--2021-03-25-VOTEHISTORY-Edit.tab", low_memory=False, sep="\t", encoding="ISO-8859-1")
print(vf.columns)
vf["General_2020_11_03"] = vf["General_2020_11_03"].fillna(0)
#vf["Runoff_2020_07_14"] = vf["Runoff_2020_07_14"].fillna(0)
vf["Primary_2020_03_03"] = vf["Primary_2020_03_03"].fillna(0)
vf["Presidential_Primary_2020_03_03"] = vf["Presidential_Primary_2020_03_03"].fillna(0)
vf = vf.replace({"Y":1})
for col in ['General_2020_11_03', 'Primary_2020_03_03', 'Presidential_Primary_2020_03_03']: #, 'Runoff_2020_07_14']:
  print(col, sum(vf[col]))

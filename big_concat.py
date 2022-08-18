import glob
import pandas as pd

my_files = glob.glob("chunks16/*voter-pred-corrected-vtd.csv")
fs = [pd.read_csv(f) for f in my_files]
print(fs[0].head())
df = pd.concat(fs)
print(len(df.VTD.unique()))
df = df.groupby("VTD").sum().reset_index()

df.to_csv("VoterPred16-v4.csv", index=False)

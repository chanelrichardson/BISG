import pandas as pd

vf_18 = pd.read_csv("VM2--TX--2021-03-25-VOTEHISTORY-Edit.tab", sep="\t", encoding="ISO-8859-1", low_memory=False)
dem_18 = pd.read_csv("VM2--TX--2021-03-25-DEMOGRAPHIC-Edit.tab", sep="\t", encoding="ISO-8859-1", low_memory=False)
vf_full = vf_18.merge(dem_18, on="LALVOTERID")

vf_full.to_csv("voterfile_20.csv", index=False)

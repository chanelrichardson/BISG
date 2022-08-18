import pandas as pd
import geopandas as gpd
import glob

#vf_20 = pd.read_csv("VM2--TX--2021-03-25-DEMOGRAPHIC-Edit.tab", chunksize=1000, low_memory=False, sep="\t", encoding='ISO-8859-1')
vf_df = pd.read_csv("voterfile_20.csv", low_memory=False) #concat(vf_20)

my_20s = glob.glob("chunks20/*header20-corrected.csv")
tot_len = sum([len(pd.read_csv(f)) for f in my_20s])
print(f"Length from glob: {tot_len}, length from voter file: {len(vf_df)}")

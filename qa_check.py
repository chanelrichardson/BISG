import pandas as pd
import geopandas as gpd
import json
import glob
tabblock = json.load(open("tabblock.json"))#pd.read_csv("TX_2020_tabblocks_052522.tab", sep="\t", low_memory=False, encoding='ISO-8859-1', dtype={"TABBLOCK":str, "AddressLine":str}).rename(columns={"TABBLOCK":"GEOID20"}).set_index("AddressLine").to_dict()["GEOID20"]

my_files = glob.glob("county-chunks18/*.csv")
for file in my_files:
  
  f = pd.read_csv(file, dtype={"Residence_Addresses_AddressLine":str})
  f["GEOID20"] = f["Residence_Addresses_AddressLine"].map(tabblock)
  print(len(f["GEOID20"][~f.GEOID20.isna()]), len(f), file)
  f.to_csv(file, index=False)
"""
headers = pd.read_csv("VoterMapping--TX--HEADERS--03-12-2017-HEADERS-Edit.tab", sep="\t", low_memory=False, encoding='ISO-8859-1', dtype={"Residence_Addresses_CensusTract":str, "Residence_Addresses_CensusBlock":str})
headers["GEOID20"] = headers["Residence_Addresses_AddressLine"].map(tabblock)
headers.to_csv("voterfile_16.csv", index=False)

demographics20 = pd.read_csv("VM2--TX--2021-03-25-DEMOGRAPHIC-Edit.tab", sep="\t", low_memory=False, encoding='ISO-8859-1', dtype={"Residence_Addresses_CensusTract":str, "Residence_Addresses_CensusBlock":str})

vhistory20 = pd.read_csv("VM2--TX--2021-03-25-VOTEHISTORY-Edit.tab", sep="\t", low_memory=False, encoding='ISO-8859-1')

merged20 = demographics20.merge(vhistory20, on = "LALVOTERID")
merged20["GEOID20"] = merged20["Residence_Addresses_AddressLine"].map(tabblock)
merged20.to_csv("voterfile_20.csv", index=False)

demographics18 = pd.read_csv("VM2--TX--2019-02-24-DEMOGRAPHIC-Edit.tab", sep="\t", low_memory=False, encoding = 'ISO-8859-1', dtype={"Residence_Addresses_AddressLine": str})
vhistory18 = pd.read_csv("VM2--TX--2019-02-24-VOTEHISTORY-Edit.tab", sep="\t", low_memory=False, encoding='ISO-8859-1')
merged18 = demographics18.merge(vhistory18, on = "LALVOTERID")
merged18['GEOID20'] = merged18["Residence_Addresses_AddressLine"].map(tabblock)
merged18.to_csv("voterfile_18.csv")
"""

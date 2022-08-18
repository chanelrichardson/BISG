import pandas as pd

vf = pd.read_csv("VoterMapping--TX--HEADERS--03-12-2017-HEADERS-Edit.tab", low_memory=False, sep="\t", encoding="ISO-8859-1")
print(vf.columns)

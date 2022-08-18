import pandas as pd

my_encoding = 'ISO-8859-1'
#vf_dem = pd.read_csv('VM2--TX--2019-02-24-DEMOGRAPHIC-Edit.tab', encoding =my_encoding, low_memory=False, sep="\t")
#vf_votes = pd.read_csv('VM2--TX--2019-02-24-VOTEHISTORY-Edit.tab', encoding=my_encoding, low_memory=False, sep="\t")
df = pd.read_csv('VM2Uniform--TX--2019-02-24.tab', encoding=my_encoding, low_memory=False, sep='\t', iterator=True, chunksize=1000)
vf = pd.concat(df, ignore_index=True)
print(vf.columns)

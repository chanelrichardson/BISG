import glob
import os

county_files = glob.glob("county-chunks20/*-header20.csv")
county_files = [file.split("/")[-1].split("-")[0] for file in county_files]
with open("BISG_kick_off.sh", "w+") as f:
  for file in county_files: 
    if file == "Harris":
      for year in [16, 18, 20]:
           f.writelines(f"python submit_jobs.py -county {file} -year {year}\n")
    
f.close()

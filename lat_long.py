import geopandas as gpd
import pandas as pd
import glob
import math
import argparse

#script to spatially join all county files to the texas shape file

parser = argparse.ArgumentParser(description="LAT-LONG-ENCODER", 
                                 prog="lat_long_BISG.py")
parser.add_argument("-county", metavar="county", type=str,
                    help="Which county to run BISG on?")
parser.add_argument("-year", metavar="year", type=str,
                    help="the county chunk year")
args = parser.parse_args()

county_str = args.county
year_str = args.year


tx = gpd.read_file("http://data.mggg.org.s3-website.us-east-2.amazonaws.com/census-2020/tx/tx_block.zip")

file = f"chunks{year_str}/{county_str}-header{year_str}.csv"

f = pd.read_csv(file, dtype={"Residence_Addresses_Latitude":float, "Residence_Addresses_Longitude":float}, low_memory=False)

my_geo_file = gpd.GeoDataFrame(
    f, geometry=gpd.points_from_xy(f.Residence_Addresses_Longitude, f.Residence_Addresses_Latitude))

my_geo_file.crs = tx.crs
tx = tx[["GEOID20", "geometry"]]
full_voter_file = gpd.sjoin(my_geo_file, tx, how="left")
f_name = file.split(".csv")[0] + "-corrected.csv"
full_voter_file = full_voter_file.drop(columns="geometry").drop_duplicates(subset=['LALVOTERID'])

assert len(f) == len(full_voter_file)

full_voter_file.to_csv(f_name, index=False)

from pandas.core.indexes import base
from core.elevation.elevation_converter import ElevationConverter
import os
import pandas as pd
from tqdm import tqdm

def merge_dfs():
    slopes = pd.read_csv("data/slopes.csv")
    dataset = pd.read_csv("data/dataset.csv")
    dataset['slope'] = slopes['slope']
    dataset = dataset[dataset['slope'] != -1]
    dataset.to_csv("data/dataset_with_slopes.csv", index=False)

def calc_slopes():
    base_dir = "data/elevation"
    merc_dir = os.path.join(base_dir, "mercator")
    landslides = pd.read_csv("data/dataset.csv")

    slopes = []

    landslides = landslides[['lat', 'lon', 'id']]
    for idx, row in tqdm(list(landslides.iterrows())):
        print()
        lat = row['lat']
        lon = row['lon']
        # print("lat: ", lat)
        # print("lon: ", lon)
        
        if int(lat) < 0:
            filename = "S"
        else:
            filename = "N"
        
        lon_letter = ""
        if int(lon) < 0:
            lon_letter = "W"
        else:
            lon_letter = "E"
        
        zero_lat = ""
        if (abs(int(lat)) < 10):
            zero_lat = "0"

        zero_lon = ""
        if (abs(int(lon)) < 100):
            zero_lon = "0"
        if (abs(int(lon)) < 10):
            zero_lon = "00"
        
        filename += f"{zero_lat}{str(abs(int(lat)))}{lon_letter}{zero_lon}{str(abs(int(lon)))}.tif"
        print("Converting " + filename)
        if not os.path.isfile(os.path.join(merc_dir, filename)):
            max_slope = -1
            print(filename + " not found. Appending -1.")
            slopes.append(max_slope)
            continue
        
        converter = ElevationConverter(base_dir, filename)
        max_slope = converter.get_slope(lat, lon)
        print("max slope: ", max_slope)
        slopes.append(max_slope)

    landslides['slope'] = slopes
    print(landslides.head())
    landslides.to_csv("data/slopes.csv")

    merge_dfs()


if __name__ == '__main__':
    # calc_slopes()
    merge_dfs()
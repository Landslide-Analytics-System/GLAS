from core.modeling.elevation_modeling import ElevationConverter
import os
import pandas as pd
from tqdm import tqdm
import logging

def main():
    base_dir = "./data/elevation"
    data_dir = os.path.join(base_dir, "elevation_data")
    landslides = pd.read_csv("./data/landslide_catalog/filtered_landslides.csv")
    # logger = logging.getLogger()

    # filter by hgts --> remove all zips. nvm not needed
    # hgts = [i for i in list(os.walk(data_dir))[0][2] if i[-1] == "t"]
    slopes = []

    landslides = landslides[['latitude', 'longitude', 'FID']]
    for idx, row in tqdm(list(landslides.iterrows())):
        print()
        lat = row['latitude']
        lon = row['longitude']
        # print("lat: ", lat)
        # print("lon: ", lon)
        
        if int(lat) < 0:
            filename = "S"
        else:
            filename = "N"
        
        zero_lat = ""
        if (int(lat) < 10):
            zero_lat = "0"

        zero_lon = ""
        if (int(lon) < 100):
            zero_lon = "0"
        if (int(lon) < 10):
            zero_lon = "00"
        
        filename += f"{zero_lat}{str(abs(int(lat)))}E{zero_lon}{str(int(lon))}.hgt"
        if not os.path.isfile(os.path.join(data_dir, filename)):
            max_slope = -1
            slopes.append(max_slope)
            continue
        
        converter = ElevationConverter(filename)
        converter.calc_slope()
        max_slope = converter.get_slope(lat, lon)
        print("max slope: ", max_slope)
        slopes.append(max_slope)

    landslides['slope'] = slopes
    print(landslides.head())
    landslides.to_csv("./data/landslide_catalog/landslides_with_slope.csv")


if __name__ == '__main__':
    main()
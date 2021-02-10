from core.elevation.elevation_to_slope_all import ElevationConverter
import os
from tqdm import tqdm

converter = ElevationConverter("data/elevation/mercator")
files = [i for i in os.listdir("data/elevation/mercator") if i[-4:]==".tif"]

for filename in tqdm(files):
    converter.ConvertToSlope(filename)
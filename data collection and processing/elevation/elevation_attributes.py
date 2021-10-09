import os
import pandas as pd
from tqdm import tqdm
from osgeo import gdal

class ElevationAttributes():
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def showSlopeMap(self, filename):
        ds = gdal.Open(os.path.join(self.data_dir, filename))
        data = ds.GetRasterBand(1).ReadAsArray()

        
df = pd.read_csv("data/updated_dataset.csv")
filenames = os.listdir("data/elevation/mercator")
print(df)
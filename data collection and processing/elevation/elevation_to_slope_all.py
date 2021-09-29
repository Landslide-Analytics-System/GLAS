import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import subprocess

class ElevationConverter:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.slope_dir = os.path.join(self.base_dir, "slope")
    
    def ConvertToSlope(self, filename):
        if not os.path.isdir(self.slope_dir):
            os.mkdir(self.slope_dir)
        #put all the filename stuff into a function so there only needs to be one class instance
        file = gdal.Open(os.path.join(self.base_dir, filename))
        try:
            elevation_data = file.GetRasterBand(1).ReadAsArray()
        except:
            print("ERROR: " + filename)
        
        slope_command = f'gdaldem slope {os.path.join(self.base_dir, filename)} {os.path.join(self.slope_dir, filename[:-4])}.tif -compute_edges'
        subprocess.call(slope_command, shell=True, stdout=subprocess.DEVNULL)
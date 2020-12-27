import os
import numpy as np
from tqdm.utils import disp_trim
from .srtm_map import MapGenerator
from ..utils.hgt_parser import HGTParser
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
import richdem as rd

class GlobalMapGenerator():
    def __init__(self):
        self.gen = MapGenerator()
        self.base_dir = "data/elevation/"
        self.hgt_files = os.listdir(self.base_dir)
        self.global_elevation_data = None
    
    def shrink(data, rows, cols):
        return data.reshape(rows, data.shape[0]/rows, cols, data.shape[1]/cols).sum(axis=1).sum(axis=2)

    def GenerateGlobalMaps(self, stride, mode):
        res = 1201//stride
        max_N = 59
        max_W = 180
        max_S = 56
        max_E = 179
        
        # N59 --> N00
        # S01 --> S56
        # E000 --> E179
        # W180 --> W001
        
        # Initialize array global elevation
        self.global_elevation_data = np.zeros(( res*(max_S+max_N+1), res*(max_E+max_W+1) ))

        print("Output Image Shape:", self.global_elevation_data.shape)

        for hgt_file in tqdm(self.hgt_files):
            lat_letter = hgt_file[0]
            lon_letter = hgt_file[3]
            lat = int(hgt_file[1:3])
            lon = int(hgt_file[4:7])

            if lat_letter == "S":
                # Shift south down by max_N, but south starts at S01 so we translate up by 1 too
                lat_trans = max_N + lat - 1
            else:
                # Bigger N lat means further up. E.g. N59 is at index 0 and is higher than N00
                lat_trans = max_N - lat
            
            if lon_letter == "E":
                # Shift east right by max_W
                lon_trans = max_W + lon
            else:
                # Bigger W lon means further left. E.g. W180 is at index 0 and is more left than W001
                lon_trans = max_W - lon

            # load in data from file as resized
            data = cv2.resize(HGTParser(os.path.join(self.base_dir, hgt_file)), (res, res))
            # data = np.array(rd.TerrainAttribute(rd.rdarray(data, no_data=-9999), "slope_riserun"))

            # generate bounds (x/y --> lon.lat for data from this file for the giant array)
            lat_bounds = [res*lat_trans, res*(lat_trans+1)]
            lon_bounds = [res*lon_trans, res*(lon_trans+1)]
            
            try:
                self.global_elevation_data[ lat_bounds[0]:lat_bounds[1],  lon_bounds[0]:lon_bounds[1] ] = data
            except:
                print("REFERENCE ERROR: " + hgt_file)
                print("lat: ", lat_bounds)
                print("lon: ", lon_bounds)
            
        self.global_slope_data = np.asarray(rd.TerrainAttribute(rd.rdarray(self.global_elevation_data, no_data=-9999), mode))
        
        # TO IMPLEMENT:
        # - logarithmic colorbar scaling
        # - OR prefill oceans as -500 and color differently
        # - OR create custom colorbar
        # - see https://matplotlib.org/3.2.1/tutorials/colors/colormapnorms.html
        
    def ShowSaveElevation(self, filepath):
        # len x width
        plt.figure(figsize=(20,8))
        plt.imshow(self.global_elevation_data, cmap="jet")
        plt.title("Global Elevation Heatmap (Non-Trimmed)")
        plt.colorbar()
        np.save(filepath+".npy", self.global_elevation_data)
        plt.savefig(filepath+".png", format = "png", dpi=500)
        plt.show()  
        # Look into rd.rdShow source code and replicate to save data/implement custom params. 
        rd.rdShow(rd.rdarray(self.global_elevation_data, no_data=-9999), cmap="jet")
        del self.global_elevation_data
    
    def ShowSaveSlope(self, filepath):
        # len x width
        plt.figure(figsize=(20,8))
        plt.imshow(self.global_slope_data)
        plt.imshow(self.global_slope_data, cmap="jet")
        plt.title("Global Slope Heatmap (Non-Trimmed)")
        plt.colorbar()
        np.save(filepath+".npy", self.global_slope_data)
        plt.savefig(filepath+".png", format = "png", dpi=500)
        plt.show()
        rd.rdShow(rd.rdarray(self.global_slope_data, no_data=-9999), cmap="jet")
import os
import numpy as np
from ..utils.hgt_parser import hgt_parser
import richdem as rd
import matplotlib.pyplot as plt
import contextlib

class MapGenerator():
    def __init__(self):
        self.base_dir = "data/elevation/"
    
    def loadData(self, filename):
        self.filename = filename
        self.elevation_data = hgt_parser(os.path.join(self.base_dir, filename))
        # self.fill_val = np.mean(np.mean(np.array(self.elevation_data), axis=1))

    def calcSlope(self, mode):
        if not hasattr(self, 'elevation_data'):
            print("Error: Asked to calc slope but no elevation file was designated.")

        if not mode in ['slope_riserun', 'slope_percentage', 'slope_degrees', 'slope_radians']:
            print("Pass in one of " + ['slope_riserun', 'slope_percentage', 'slope_degrees', 'slope_radians'])
        self.elevation_filled = rd.rdarray(self.elevation_data, no_data=-9999)
        
        with contextlib.redirect_stdout(None):
            self.slope_data_numpy = np.array(rd.TerrainAttribute(self.elevation_filled, attrib=mode))

    def showElevationMap(self):
        plt.imshow(self.elevation_filled, interpolation="none", cmap="magma")
        plt.title(self.filename[:-4] + " Elevation Map")
        plt.colorbar()
        plt.show()
    

    def showSlopeMap(self):
        self.slope_data = rd.rdarray(self.slope_data_numpy, no_data=-9999)
        plt.imshow(self.slope_data, interpolation="none", cmap="magma")
        plt.title(self.filename[:-4] + " Slope Map")
        plt.colorbar()
        plt.show()
    
    def saveElevationMap(self):
        # need to implement
        pass

    def saveSlopeMap(self):
        # need to implement
        pass
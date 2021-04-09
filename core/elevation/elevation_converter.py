import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import subprocess
import rasterio

def decdeg2dms(dd):
   is_positive = float(dd) >= 0
   dd = abs(float(dd))
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)


class ElevationConverter:
    def __init__(self, base_dir, filename):
        self.base_dir = base_dir
        self.merc_dir = os.path.join(self.base_dir, "mercator")
        
        #put all the filename stuff into a function so there only needs to be one class instance
        self.filename = filename
        self.file = gdal.Open(os.path.join(self.merc_dir, self.filename))
        self.elevation_data = self.file.GetRasterBand(1).ReadAsArray()

        slope_command = f'gdaldem slope {os.path.join(self.merc_dir, self.filename)} "interm_slope.tif" -compute_edges'
        subprocess.call(slope_command, shell=True, stdout=subprocess.DEVNULL)
        
        with rasterio.open("interm_slope.tif") as f:
            self.slope_data = f.read(1)
            # print(self.slope_data)

        subprocess.call("rm interm_slope.tif", shell=True)

        
    def get_slope(self, lat, lon):
        # fixed this so that it properly gets slope from mercator projection
        # get array idx from dms, and then use proportions to get same bbox in mercator projected slope

        lat_degs, lat_mins, lat_secs = decdeg2dms(lat)
        lon_degs, lon_mins, lon_secs = decdeg2dms(lon)

        lat_secs += 60 * lat_mins
        lat_secs /= 3
        lon_secs += 60 * lon_mins
        lon_secs /= 3

        # convert from seconds to x/y for array indexing
        x = int(lon_secs)
        y = 1201 - int(lat_secs)
        distance = 33 # ensures 1x1 mile bbox

        height = len(self.slope_data)
        width = len(self.slope_data[0])
        xvals = [max(0, round(width * (x-distance)/1200)), min(width, round(width * (x+distance)/1200))]
        yvals =  [max(0, round(height * (y-distance)/1200)), min(height, round(height * (y+distance)/1200))]

        # area_slice = self.slope_data[max(0, yvals[0]) : min(height, yvals[1])]
        # area_slice = area_slice[:, max(0, xvals[1]) : min(width, xvals[0])]

        area_slice = self.slope_data[yvals[0] : yvals[1]]
        area_slice = area_slice[:, xvals[0] : xvals[1]]

        # making sure slope is + (- slope just means its in another direction - magnitude is what matters)
        area_slice = np.abs(area_slice)
        print(area_slice)

        if area_slice.size == 0:
            slope_to_return = -1
            print("area slice has size 0")
        else:
            slope_to_return = np.percentile(area_slice.flatten(), 95)
            assert slope_to_return >= 0, "95th percentile slope is less than 0"

        return round(slope_to_return, 3)
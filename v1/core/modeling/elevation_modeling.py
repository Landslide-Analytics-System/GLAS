import os
import numpy as np
import richdem as rd
import matplotlib.pyplot as plt
from array import array

class srtmParser(object):
    def parseFile(self,filename):
        f = open(filename, 'rb')
        format = 'h'
        row_length = 1201
        data = array(format)
        data.fromfile(f, row_length*row_length)
        data.byteswap()
        f.close()
        data = np.array(data)
        data = np.reshape(data, (1201, 1201))
        return data


def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)


class ElevationConverter:
    def __init__(self, filename):
        self.base_dir = "./data/elevation"
        self.data_dir = os.path.join(self.base_dir, "elevation_data")
        self.filename = filename
        self.parser = srtmParser()
        self.elevation_data = self.parser.parseFile(os.path.join(self.data_dir, self.filename))
        self.fill_val = np.mean(np.mean(np.array(self.elevation_data), axis=1))

        # removing broken data points with the average of remaining elements. sorta works?
        # for r, row in enumerate(self.elevation_data):
        #     for c, val in enumerate(row):
        #         # sanity check --> height of mount everest is ~8800 m
        #         if val > 9000 or val < 0:
        #             self.elevation_data[r][c] = self.fill_val - val/(1201*1201)
        #             self.fill_val = np.mean(np.mean(np.array(self.elevation_data), axis=1))
        #             print("-----------------REPLACED-----------------------")


    def calc_slope(self):
        elevations = rd.rdarray(self.elevation_data, no_data=self.fill_val)
        self.slope_data = np.array(rd.TerrainAttribute(elevations, attrib='slope_riserun'))

    def show_image(self):
        elevations = rd.rdarray(self.elevation_data, no_data=self.fill_val)
        plt.imshow(elevations, interpolation="bilinear", cmap="magma")
        plt.title(self.filename[:-4] + " Elevation Map")
        plt.colorbar()
        plt.show()
    
    def show_slope(self):
        slopes = rd.rdarray(self.slope_data, no_data=self.fill_val)
        rd.rdShow(slopes, cmap = "magma")
        # plt.title(self.filename[:-4] + " Slope Map")
        # plt.colorbar()
        plt.show()
    
    def show_aspect(self):
        elevations = rd.rdarray(self.elevation_data, no_data=self.fill_val)
        aspect = rd.TerrainAttribute(elevations, attrib='aspect')
        rd.rdShow(aspect, axes=False, cmap='Blues', figsize=(8, 5.5))
        plt.show()
    
    def slope_to_csv(self):
        if not os.path.exists(os.path.join(self.base_dir, "slopes")):
            os.mkdir(os.path.join(self.base_dir, "slopes"))
        print(self.elevation_data)
        np.savetxt(os.path.join(self.base_dir, "slopes", self.filename[:-4] + ".csv"), self.elevation_data, delimiter=",")
    
    def get_slope(self, lat, lon):
        lat_degs, lat_mins, lat_secs = decdeg2dms(lat)
        lon_degs, lon_mins, lon_secs = decdeg2dms(lon)

        lat_secs += 60 * lat_mins
        lat_secs /= 3
        lon_secs += 60 * lon_mins
        lon_secs /= 3

        # convert from seconds to x/y for array indexing
        x = int(lon_secs)
        y = 1201 - int(lat_secs)
        distance = 25

        area_slice = self.slope_data[ max(0, y-distance) : min(1200, y+distance) ]
        area_slice = area_slice[:, max(0, x-distance) : min(1200, x+distance)]

        slope_to_return = np.percentile(area_slice.flatten(), 95)
        # max_slope = max([ max([i for i in j]) for j in area_slice ])
        if slope_to_return < 0:
            return -1
        return int(slope_to_return)
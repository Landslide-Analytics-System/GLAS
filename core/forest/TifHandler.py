import PIL
from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = 10**10
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show

class TifHandler:
    def __init__(self, f_name):
        self.f_name = f_name
        self.ar = np.array(Image.open("TIF Files/"+f_name))
        self.f1 = -1 if f_name[-5] == 'W' else 1
        self.f0 = -1 if f_name[-10] == 'S' else 1
        self.top_left = [int(f_name[-12:-10]) * self.f0, int(f_name[-8:-5]) * self.f1]
        self.bottom_right = [self.top_left[0] - 10, self.top_left[1]+10]
        print(self.top_left, self.bottom_right)
        self.pixPerMile = int(4000/69)
        print("      ====== Finished reading ======")

    def shape(self):
        print(self.ar.shape)

    def forestLoss(self, year, lat, lon, radius = 5):
        '''
        ar[0] is the topmost latitude.
        col 0 is the leftmost longitude
        ar[0][0] is the top left corner
        1. Should we do <= year or < year. For example, if forest loss happened end of 2017, landslide 
            beginning of 2017. Then <= counts forest loss for that landslide.
        '''
        year -= 2000
        newLat = self.top_left[0] - lat
        newLon = lon - self.top_left[1]
        radius *= self.pixPerMile
        for i in range(0, radius):
            x = int(newLat * 4000+i-radius/2)
            if x >= 40000 or x < 0:
                continue
            for j in range(0, radius):
                y = int(newLon * 4000+j-radius/2)
                if y >= 40000 or y < 0:
                    continue
    #             print(x,y)
    #             print(ar[x][y], end =' ')
                if self.ar[x][y] != 0 and self.ar[x][y] <= year:
                    return True, 2000 +self.ar[x][y]
    #         print("")
        return False, 0

    def inBounds(self, lat, lon):
        return lat >= self.bottom_right[0] and lat <= self.top_left[0] and lon >= self.top_left[1] and lon <= self.bottom_right[1]

    def resStats(self):
        print(self.pixPerMile, "pixels in a mile.")

    def thumbnail(self, show = False):
        values = []
        for i in range(0, 40000, 100):
            temp = []
            for j in range(0, 40000, 100):
                temp.append(self.ar[i][j])
            values.append(temp)
        values = np.array(values)
        
        print("      ---- Created thumbnail ----")
        return values

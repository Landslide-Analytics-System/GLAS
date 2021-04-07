import numpy as np
import PIL
from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = 10**10


class TifHandler:
    def __init__(self, f_name):
        self.f_name = f_name
        self.ar = np.array(Image.open(f_name))
        self.f0 = -1 if f_name[-10] == 'S' else 1
        self.f1 = -1 if f_name[-5] == 'W' else 1
        self.top_left = [int(f_name[-12:-10]) * self.f0,
                         int(f_name[-8:-5]) * self.f1]
        self.bottom_right = [self.top_left[0] - 10, self.top_left[1]+10]
        print(self.top_left, self.bottom_right)
        self.pixPerMile = int(4000/69)
        print("      ====== Finished reading ======")

    def shape(self):
        print(self.ar.shape)

    def forestLoss(self, year, lat, lon, radius=5):
        year -= 2000
        newLat = self.top_left[0] - lat
        newLon = lon - self.top_left[1]
        radius *= self.pixPerMile
        greatest = 0
        for i in range(0, radius):
            x = int(newLat * 4000+i-radius/2)
            if x >= 40000 or x < 0:
                continue
            for j in range(0, radius):
                y = int(newLon * 4000+j-radius/2)
                if y >= 40000 or y < 0:
                    continue
                if self.ar[x][y] != 0 and self.ar[x][y] < year:
                    greatest = max(greatest, self.ar[x][y])
                    # return True, 2000 + self.ar[x][y]
        return (greatest < year and greatest != 0), greatest

    def inBounds(self, lat, lon):
        return lat >= self.bottom_right[0] and lat <= self.top_left[0] and lon >= self.top_left[1] and lon <= self.bottom_right[1]

    def resStats(self):
        print(self.pixPerMile, "pixels in a mile.")

    def thumbnail(self, show=False):
        values = []
        for i in range(0, 40000, 100):
            temp = []
            for j in range(0, 40000, 100):
                temp.append(self.ar[i][j])
            values.append(temp)
        values = np.array(values)

        print("      ---- Created thumbnail ----")
        return values

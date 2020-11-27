import struct
import numpy as np
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
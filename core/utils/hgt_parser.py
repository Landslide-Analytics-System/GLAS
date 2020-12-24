import numpy as np
from array import array

def hgt_parser(filepath):
        with open(filepath, 'rb') as fin:
            format = 'h'
            row_length = 1201
            data = array(format)
            data.fromfile(fin, row_length*row_length)
            data.byteswap()

        data = np.array(data)
        data = np.reshape(data, (row_length, row_length))
        return data
from core.modeling.elevation_modeling import ElevationConverter
import os
import pandas as pd
from tqdm import tqdm
import logging

def main():
    converter = ElevationConverter("N26E073.hgt")
    converter.calc_slope()
    converter.show_image()
    converter.show_slope()

if __name__ == '__main__':
    main()
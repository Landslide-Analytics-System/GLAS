from core.modeling.elevation_modeling import ElevationConverter
import os

def main():
    base_dir = "./data/elevation"
    data_dir = os.path.join(base_dir, "elevation_data")
    # filter by hgts --> remove all zips
    hgts = [i for i in list(os.walk(data_dir))[0][2] if i[-1] == "t"]

    converter = ElevationConverter("N30E079.hgt")
    converter.show_image()
    converter.calc_slope()
    converter.get_slope(30.7346, 79.0669)
    # converter.show_image()
    converter.show_slope()
if __name__ == '__main__':
    main()
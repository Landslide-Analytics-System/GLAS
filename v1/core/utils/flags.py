import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--precip_data_save_loc', type=str, default='./data/precip_data')

FLAGS = parser.parse_args()
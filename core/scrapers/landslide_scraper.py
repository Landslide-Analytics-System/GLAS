import os
import argparse
import requests
from tqdm import tqdm

class LandslideScraper:
    def __init__(self):
        self.csv_url = "https://opendata.arcgis.com/datasets/da67f0094eea4128855b0b54ccd99e26_0.csv"
        parser = argparse.ArgumentParser()
        parser.add_argument("--save_loc", type=str, default="./data/landslide_catalog")
        self.flags = parser.parse_args()

    def download_data(self):
        # print("Downloading data from " + self.csv_url)
        req = requests.get(self.csv_url, stream=True)
        chunkSize = 1024
        filepath = os.path.join(self.flags.save_loc, "landslide_catalog.csv")

        with open(filepath, 'wb') as csv_file:
            pbar = tqdm(total=int(req.headers['Content-Length']))
            
            for chunk in req.iter_content(chunk_size=chunkSize): 
                if chunk: # filter out keep-alive new chunks
                    pbar.update (len(chunk))
                    csv_file.write(chunk)
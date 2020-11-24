import os
import argparse
import requests
import re
from tqdm import tqdm
import logging


"""
Tools for downloading and unzipping/sorting elevation data

Relevant resources:
Hub for SRTM (Shuttle Radar Topography Mission) data urls: https://wiki.openstreetmap.org/wiki/SRTM


"""


class ElevationScraper:
    def __init__(self):
        self.data_url = "http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm"
        self.base_dir = "./data/elevation/"
        self.elevation_dir = os.path.join(self.base_dir, "elevation_data")


    def download_data(self):
        # get html from self.data_url and get all urls in the html code
        req = requests.get(self.data_url)
        urls = re.findall(r"\"(https?://\S+)\"", str(req.text))

        # first four are irrelevant links so remove those. then make urls.txt file of urls
        urls = urls[4:]
        with open(os.path.join(self.base_dir, "urls.txt"), "w") as url_file:
            for url in urls:
                url_file.write(url + "\n")
        
        if not os.path.exists(self.elevation_dir):
            os.mkdir(self.elevation_dir)
        
        print("Downloading " + str(len(urls)) + " data files to " + self.elevation_dir + " from " + self.data_url)

        # downloading all zip files
        for url in tqdm(urls):
            filename = url.split("/")[-1]
            req = requests.get(url)
            with open(os.path.join(self.elevation_dir, filename), "wb") as data_file:
                data_file.write(req.content)
        print("Finished downloading zip files.")
    
    def unzip_all(self):
        pass
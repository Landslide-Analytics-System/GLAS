import os
import argparse
import requests
import re
from tqdm import tqdm
import logging
from zipfile import ZipFile
"""
Tools for downloading and unzipping/sorting elevation data

Relevant resources:
Hub for SRTM (Shuttle Radar Topography Mission) data urls: https://wiki.openstreetmap.org/wiki/SRTM

The urls.txt file was manually created to have all the download links for elevation data for Southeast Asia
(betweeen 60 East and 150 East, and -10 S to 40 N)
"""


class ElevationScraper:
    def __init__(self):
        self.data_url = "http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm"
        self.base_dir = "./data/elevation/"
        self.data_dir = os.path.join(self.base_dir, "elevation_data")
        logging.getLogger("requests").setLevel(logging.WARNING)


    def download_from_urls(self):
        # OLD METHOD: get html from self.data_url and get all urls in the html code. first four are irrelevant links so remove those. then make urls.txt file of urls
        # req = requests.get(self.data_url)
        # urls = re.findall(r"\"(https?://\S+)\"", str(req.text))
        # urls = urls[4:]

        # Get urls from urls.txt and download all those zip files
        
        with open(os.path.join(self.base_dir, "urls.txt"), "r") as url_file:
            urls = url_file.readlines()
            # remove \n character
            urls = [i[:-1] for i in urls]
        print(urls)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        
        print("Downloading " + str(len(urls)) + " data files to " + self.data_dir + " from " + self.data_url)

        # downloading all zip files
        for url in tqdm(urls):
            filename = url.split("/")[-1]
            req = requests.get(url)
            with open(os.path.join(self.data_dir, filename), "wb") as data_file:
                data_file.write(req.content)
        print("Finished downloading zip files.")
    
    def unzip_all(self):

        files = [f for f in os.listdir(self.data_dir) if os.path.isfile(os.path.join(self.data_dir, f))]
        # print(files)
        print("Unzipping " + str(len(files)) + " files")

        for filename in tqdm(files):
            zf = ZipFile(os.path.join(self.data_dir, filename), 'r')
            zf.extractall(self.data_dir)
            zf.close()
            # os.remove(os.path.join(self.data_dir, filename))
    print("Finished unzipping files")
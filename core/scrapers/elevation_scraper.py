import browser_cookie3
import requests
import os
from tqdm import tqdm
import re
import zipfile

class ElevationScraper:
    def __init__(self) -> None:
        self.base_url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL3.003/2000.02.11/"
        self.demo_url = self.base_url + "N06W001.SRTMGL3.hgt.zip"
        self.url_pages = [self.base_url + "SRTMGL3_page_{0}.html".format(i) for i in range(1, 7)]
        self.hgt_urls = []
        self.badFiles = []
        self.base_dir = "data/elevation/"

        if not os.path.isdir(self.base_dir):
            os.mkdir(self.base_dir)
    
    def getUrls(self):
        # get all urls ending with "hgt.zip" from the six pages
        print("Finding hgt files...")
        url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        for url in tqdm(self.url_pages):
            r = requests.get(url)
            self.hgt_urls.extend(re.findall(url_regex, r.text))
        self.hgt_urls = [i for i in self.hgt_urls if i[-7:] == "hgt.zip"]
        print("Found " + str(len(self.hgt_urls)) + " hgt files to download.")

        # with open("url_list.txt", "w") as fout:
        #     for i in self.hgt_urls:
        #         fout.write(i+"\n")

    def launchFirefox(self):
        os.system("new firefox -new-window " + self.demo_url)
    
    def getCredentials(self):
        self.cookies = browser_cookie3.firefox(domain_name="usgs.gov")
    
    def downloadFile(self, fileURL):
        # code to download file and save to "data/elevation" directory
        r = requests.get(fileURL, cookies = self.cookies)
        if "Denied" in r.text:
            print(r.text)
            return

        with open( os.path.join(self.base_dir, fileURL.split("/")[-1]), "wb") as fout:
            fout.write(r.content)

    def downloadAll(self):
        # make for loop to download all files
        for fileURL in tqdm(self.hgt_urls):
            if not os.path.isfile( os.path.join(self.base_dir, fileURL.split("/")[-1]) ):
                self.downloadFile(fileURL)

    def findBadFiles(self):
        for filename in os.listdir(self.base_dir):
            if os.path.getsize( os.path.join(self.base_dir, filename) ) < 1000:
                print("WARNING: " + filename + " has less than 1 kilobyte of data.")
                self.badFiles.append(filename)

    def fixBadFiles(self):
        for filename in self.badFiles:
            self.downloadFile(self.base_url + filename)
    
    def unzipAll(self):
        hgt_files = os.listdir(self.base_dir)
        for hgt_file in hgt_files:
            with zipfile.ZipFile(os.path.join(self.base_dir, hgt_file), "r") as zip_ref:
                zip_ref.extractall(self.base_dir)
                # os.remove( os.path.join(self.base_dir, hgt_file) )
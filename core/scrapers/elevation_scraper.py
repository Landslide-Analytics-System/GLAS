from http import cookiejar
import browser_cookie3
import requests
import os
from tqdm import tqdm
import re

# todo: add progress bar

class ElevationScraper:
    def __init__(self) -> None:
        self.base_url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/"
        self.demo_url = self.base_url + "N06W001.SRTMGL1.hgt.zip"
        self.url_pages = [self.base_url + "SRTMGL1_page_{0}.html".format(i) for i in range(1, 7)]
        self.hgt_urls = []

        if not os.path.isdir("data/elevation/"):
            os.mkdir("data/elevation/")
    
    def getUrls(self):
        print("Finding hgt files...")
        url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        for url in self.url_pages:
            r = requests.get(url)
            self.hgt_urls.extend(re.findall(url_regex, r.text))
        self.hgt_urls = [i for i in self.hgt_urls if i[-7:] == "hgt.zip"]
        print("Found " + str(len(self.hgt_urls)) + " hgt files to download.")

        with open("url_list.txt", "w") as fout:
            for i in self.hgt_urls:
                fout.write(i+"\n")

    def getCredentials(self):
        self.cookies = browser_cookie3.firefox(domain_name="usgs.gov")
        # os.system("firefox -new-window " + self.demo_url)
    
    def downloadFile(self, fileURL):
        # code to download file and save to "data/elevation" directory
        r = requests.get(fileURL, cookies = self.cookies)
        with open("data/elevation/"+fileURL.split("/")[-1], "wb") as fout:
            fout.write(r.content)

    def downloadAll(self):
        # make for loop to download all files
        for fileURL in tqdm(self.hgt_urls):
            if not os.path.isfile("data/elevation/"+fileURL.split("/")[-1]):
                self.downloadFile(fileURL)
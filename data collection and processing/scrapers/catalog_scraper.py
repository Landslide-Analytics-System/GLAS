import requests
import os

class CatalogScraper():
    def __init__(self):
        self.base_dir = "data/landslide_catalog/"
        # name: download URL
        self.catalogs = {
            "Global LC": "https://opendata.arcgis.com/datasets/da67f0094eea4128855b0b54ccd99e26_0.csv",
            # "Nepal LC": "NA"
        }
        if not os.path.isdir(self.base_dir):
            os.mkdir(self.base_dir)
    
    def downloadCatalog(self, catalog_name):
        r = requests.get(self.catalogs[catalog_name])
        with open(os.path.join(self.base_dir, catalog_name+".csv"), "w") as catalog:
            catalog.write(r.text)
    
    def downloadAll(self):
        for catalog_name in self.catalogs:
            self.downloadCatalog(catalog_name)
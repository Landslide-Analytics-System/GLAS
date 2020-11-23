import os
import argparse
import requests
# from tqdm import tqdm

"""
Data sources for Global Landslide Catalog.
We need to look at these to determine which is best to use or merge them.
Some don't have full names for columns

source:
    source_link
    direct_download_link
    num_rows

data.world:
    https://data.world/nasa/global-landslide-catalog
    no direct link. click button to download
    9565

data.nasa.gov:
    https://data.nasa.gov/Earth-Science/Global-Landslide-Catalog/h9d8-neg4
    https://data.nasa.gov/api/views/9ns5-uuif/rows.csv?accessType=DOWNLOAD
    6789

data.nasa.gov 2:
    https://data.nasa.gov/Earth-Science/Global-Landslide-Data-Export-Visual-Explorer/angv-aquq
    https://data.nasa.gov/api/views/dd9e-wu2v/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*
    11033

arcgis:
    https://hub.arcgis.com/datasets/da67f0094eea4128855b0b54ccd99e26_0
    https://opendata.arcgis.com/datasets/da67f0094eea4128855b0b54ccd99e26_0.csv
    13492

catalog.data.gov:
    https://catalog.data.gov/dataset/global-landslide-catalog-export
    https://data.nasa.gov/api/views/dd9e-wu2v/rows.csv?accessType=DOWNLOAD
    11034
"""

class LandslideScraper:
    def __init__(self):
        self.csv_url = "https://data.nasa.gov/api/views/9ns5-uuif/rows.csv?accessType=DOWNLOAD"
        self.base_dir = "./data/landslide_catalog"

    def download_data(self):
        req = requests.get(self.csv_url)
        filepath = os.path.join(self.base_dir, "landslide_catalog.csv")
        
        with open(filepath, 'wb') as csv_file:
            csv_file.write(req.content)
        print("Data directory: " + self.base_dir + "landslide_catalog.csv")
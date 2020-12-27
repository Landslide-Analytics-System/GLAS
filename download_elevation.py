import os
import kaggle

kaggle.api.authenticate()
kaggle.api.dataset_download_files("shreyj1729/srtmgl3", path="data/", unzip=True)
# os.system("mv data/elevation/elevation*.zip data/elevation/")
# os.rmdir("data/elevation/elevation")

"""
The below code scrapes all the files from LP DAAC, which is slow. The same files have been uploaded to kaggle:
https://www.kaggle.com/shreyj1729/srtmgl3. The above code downloads from there.
Or you can manually download using kaggle CLI: kaggle datasets download shreyj1729/srtmgl3
"""
# from core.scrapers.elevation_scraper import ElevationScraper

# scraper = ElevationScraper()

# scraper.getUrls()

# print("Waiting for user to finish storing credentials as cookies...")
# print("This url will automatically open in firefox: https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/N06W001.SRTMGL1.hgt.zip.")
# print("Hit ENTER to continue once ready")
# input()

# scraper.launchFirefox()
# print("Hit ENTER once firefox launches.")
# print("The program will automatically find your firefox cookies and use them.")
# input()

# scraper.getCredentials()
# scraper.downloadAll()
# scraper.findBadFiles()
# scraper.fixBadFiles()
# scraper.unzipAll()
# scraper.cleanUp()
from selenium import webdriver
import pandas as pd
import os
import sys
from time import sleep
from contextlib import contextmanager
from webdriver_manager.chrome import ChromeDriverManager


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stdout


browser = None
browser = None
with suppress_stdout():
    # Will install latest version or used cached version if already present.
    # /Volumes/Seagate/Mac/Documents/Science Fair/2020/OSM
    chromeOptions = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": "/Volumes/Seagate/Mac/Documents/Science Fair/2020/OSM"}
    chromeOptions.add_experimental_option("prefs", prefs)
    # chromedriver = "path/to/chromedriver.exe"
    browser = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chromeOptions)
    print("\033[A                             \033[A")


df = pd.read_csv("dataset.csv")
finishedA = open("finished.txt", "r")
dif = 0.007
content = finishedA.read()
for idx, row in df.iterrows():
    if idx <= int(content):
        continue
    id = row.id
    lat = row.lat
    lon = row.lon
    a1 = lat - dif
    a2 = lat + dif
    b1 = lon - dif
    b2 = lon + dif
    url = "https://api.openstreetmap.org/api/0.6/map?bbox={},{},{},{}".format(
        b1, a1, b2, a2)
    print(id, " | ", lat, lon)
    browser.get(url)
    sleep(2)
    file = open("finished.txt", "w+")
    file.write(str(idx))

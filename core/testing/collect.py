import requests
import os
import datetime
import sys
from dateutil import parser
from Collector import Collector
from TifHandler import TifHandler
from DataExtractor import DataExtractor
import pandas as pd
from time import sleep
from contextlib import contextmanager
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from OSMHandler import OSMHandler

file = open("input.txt", "r")

def rnd(n, p):
    return round(n * 10**p)/(10**p)

# input: array of 11 precipitations 15 - 5
# return: array of ARI from 5 - 9
def getARI(precip):
    precip.reverse()
    # now idx 0 is precipitation for 5 days before.
    aris = []
    for day in range(0, 5):
        w = 0
        num = 0
        for t in range(7):
            w_t = pow(t+1, -2)
            w += w_t
            num += w_t * float(precip[t + day])
        aris.append(rnd(num, 9))
    return aris


write = []
columns = ["date", "lat", "lon"]
for i in range(15, 4, -1):
    columns.append("precip" + str(i))
    columns.append("temp" + str(i))
    columns.append("air" + str(i))
    columns.append("humidity" + str(i))
    columns.append("wind" + str(i))

for i in range(5, 10):
    columns.append("ari" + str(i))
columns.append("osm")
columns.append("slope")
columns.append("forest2")
df = pd.DataFrame(columns=columns)
dif = 0.006
tags = []
tagF = open("tags.txt", "r")
tags = tagF.read().split(", ")
for idx, line in enumerate(file.readlines()):
    line = line.strip()
    lat = str(line.split(" ")[0])
    lon = str(line.split(" ")[1])
    date = str(line.split(" ")[2])
    print(date, lat, lon)
    oID = lat + "," + lon

    c = Collector(lat, lon, date)
    weather = [date, lat, lon]
    weather.extend(c.getData())
    precip = []
    for i in range(3, len(weather), 5):
        precip.append(weather[i])

    content = weather
    aris = getARI(precip)

    # the first 55 columns in content are for precip15, temp15, ..... precip5, temp5, air5, humid5, wind5
    # The next 5 columns are ari5, ari6, ari7, ari8, ari9
    # the next column is street data.
    # forest data hasn't been added yet.
    content.extend(aris)

    lat = float(line.split(" ")[0])
    lon = float(line.split(" ")[1])
    date = str(line.split(" ")[2])
    handler = OSMHandler(tags)
    a1 = lat - dif
    a2 = lat + dif
    b1 = lon - dif
    b2 = lon + dif
    url = "https://api.openstreetmap.org/api/0.6/map?bbox={},{},{},{}".format(
        b1, a1, b2, a2)

    r = requests.get(url)
    f_name = "temp.osm"
    open(f_name, 'w').close()
    with open(f_name, 'wb') as f:
        f.write(r.content)
    handler.apply_file(f_name)

    count = handler.count()
    content.append(count)
    # Slope here

    # Uncomment the following lines if you have the TIF Files. Then provide the file name on the line below.
    # f_name = ""
    # tif = TifHandler(fname)
    # year = 2000 + int(date[-2:])
    # results = tif.forestLoss(year, lat, lon)
    # # results[0] is forest2. results[1] is forest_year
    # # print(results[0], results[1])
    # content.extend(results[0])
    df.loc[idx] = content

print(df)
df.to_csv("file.csv")
import requests
from Collector import Collector
from TifHandler import TifHandler
import pandas as pd
from OSMHandler import OSMHandler
import os
import pandas as pd
from elevation_converter import ElevationConverter
import os
import pandas as pd

file = open("input.txt", "r")

# Provide a list of the TIF file names that go along with each landslide in input.txt
fnames = ["Hansen_GFC-2019-v1.7_treecover2000_00N_120E.tif",
"Hansen_GFC-2019-v1.7_treecover2000_30N_070E.tif",
"Hansen_GFC-2019-v1.7_treecover2000_30N_160W.tif",
]

def rnd(n, p):
    return round(n * 10**p)/(10**p)



def getSlope(lat, lon):
    base_dir = "../../data/elevation"
    merc_dir = os.path.join(base_dir, "mercator")
    if float(lat) < 0:
        filename = "S"
    else:
        filename = "N"
        
    lon_letter = ""
    if float(lon) < 0:
        lon_letter = "W"
    else:
        lon_letter = "E"
        
    zero_lat = ""
    if (abs(float(lat)) < 10):
        zero_lat = "0"

    zero_lon = ""
    if (abs(float(lon)) < 100):
        zero_lon = "0"
    if (abs(float(lon)) < 10):
        zero_lon = "00"
        
    filename += f"{zero_lat}{str(abs(int(float(lat))))}{lon_letter}{zero_lon}{str(abs(int(float(lon))))}.tif"
    # print("Converting " + filename)
    if not os.path.isfile(os.path.join(merc_dir, filename)):
        print(filename + " not found. Appending -1.")
        return -1

    converter = ElevationConverter(base_dir, filename)
    max_slope = converter.get_slope(lat, lon)
    return max_slope

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
columns.append("landslide")
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
    # followed by slope data
    # then forest loss data
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
    # Slope comes here. Add it to the content array
    content.append(getSlope(lat, lon))

    fname = fnames[idx]
    tif = TifHandler(fname)
    year = 2000 + int(date[-2:])
    results = tif.forestLoss(year, lat, lon)
    content.append(1 if results[0] else 0)
    content.append(1)
    df.loc[idx] = content

print(df)
df.to_csv("file.csv")
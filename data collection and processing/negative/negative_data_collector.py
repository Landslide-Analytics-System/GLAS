from datetime import datetime
import requests
import os
import math
import pandas as pd
from time import sleep
from datetime import timedelta
from dateutil import parser
import random as rand
apikey = "d3a171ac3e404bfe8ca141634212101"
api_format = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + apikey + '&date='


def format_date(s):
    return s.replace("/", "-")


df = pd.read_csv("dataset.csv")
df.drop([i for i in range(10000)])


def gen_query(lat, lon, date, days_in_advance=7):
    date_list = []
    params_list = []
    for i in range(days_in_advance + 1):
        temp_date = str(parser.parse(date) - timedelta(i))[:10]
        date_list.append(temp_date)
        params_list.append(temp_date+"&q="+lat+","+lon)
    return (date_list, params_list)


def dist(lat1, lon1, lat2, lon2, rad=6):
    distance = math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)
    return distance * 69 <= rad


def distY(y1, y2, range=15):
    try:
        parts = y1.split("/")
        if(len(parts[0]) == 1):
            parts[0] = "0" + parts[0]
        if(len(parts[1]) == 1):
            parts[1] = "0" + parts[1]
        parts[2] = "20" + parts[2]
        y1 = parts[0] + "/" + parts[1] + "/" + parts[2]
        date_format = "%m/%d/%Y"
        a = datetime.strptime(y1, date_format)
        b = datetime(int(y2[:4]), int(y2[5:7]), int(y2[8:10]))
        delta = b - a
        return abs(delta.days) <= range  # that's it
    except Exception as e:
        return 1000


if not os.path.exists("Data"):
    os.makedirs("Data")

done = 0
while done < 8000:
    print(done)
    decimals = 4
    lat = str(float(rand.randint(-60*10**4, 60*10**4))/float(10**4))
    lon = str(float(rand.randint(-180*10**4, 180*10**4))/float(10**4))
    year = str(rand.randint(2009, 2020))
    month = str(rand.randint(1, 12))
    if len(month) < 2:
        month = "0"+month
    upTo = 28 if month == "02" else 30
    day = str(rand.randint(1, upTo))
    if len(day) < 2:
        day = "0"+day
    date = format_date(year+"/"+month+"/"+day)

    bad = False
    for idx, row in df.iterrows():
        distance = dist(row.lat, row.lon, float(lat), float(lon))
        gap = distY(row.date, date)
        if gap and distance:
            bad = True
            break
    if bad:
        print("  B")
        continue
    else:
        print("Doing", date, lat, lon)
    file_names, params = gen_query(lat, lon, date)
    id = str(len(os.listdir("Data")))
    did = True
    for file_name, param in zip(file_names, params):
        api_call = api_format + param

        resp = requests.get(api_call)
        if("error" in str(resp.content) or "Unable" in str(resp.content)):
            did = False
            print("Aborting....")
            break

        if not os.path.exists("Data/"+id):
            os.makedirs("Data/"+id)
        f_name = "Data/"+id+"/"+file_name+".xml"
        file = open(f_name, 'w+')
        file.write(str(resp.content))
        file.close()
    if not did:
        continue
    file = open("Data/" + id+"/info.txt", "w+")
    file.write(lat + "," + lon + " | " + date)
    file.close()
    done += 1

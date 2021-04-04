import requests
import os
import datetime
from dateutil import parser
from DataExtractor import DataExtractor


class Collector:
    def __init__(self, lat, lon, date):
        self.apikey = "d7d38893c3644b57a4a00459210404"
        self.api_format = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + \
            self.apikey + '&date='
        self.lat = lat
        self.lon = lon
        self.date = date
        self.oID = lat + "," + lon

    def getData(self):
        file_names, params = self.gen_query(self.lat, self.lon, self.date)
        file_names.reverse()
        params.reverse()
        weather = []
        for file_name, param in zip(file_names, params):
            api_call = self.api_format + param
            resp = requests.get(api_call)
            d = DataExtractor(self.oID, resp.content)
            weather.extend([d.maxPrecip(), d.maxTemp(),
                            d.maxAirPressure(), d.maxHumidity(), d.maxWind()])
        return weather

    def gen_query(self, lat, lon, date, days_in_advance=15):
        date_list = []
        params_list = []
        for i in range(5, days_in_advance + 1):
            temp_date = str(parser.parse(date) - datetime.timedelta(i))[:10]
            date_list.append(temp_date)
            params_list.append(temp_date+"&q="+lat+","+lon)
        return (date_list, params_list)

    def format_date(self, s):
        return s.replace("/", "-")

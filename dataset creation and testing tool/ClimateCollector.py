import requests
import os
import datetime
from dateutil import parser
from DataExtractor import DataExtractor


params = {
    'access_key': key,
    'query': lat+","+lon,
    'historical_date': date,
    'hourly': '1',
    'interval': '1',
}
api_result = requests.get(
    'https://api.weatherstack.com/historical', params)
api_response = api_result.json()
d = DataExtractor(api_response['historical'][date])
stuff += d.getPrecip() + "," + d.getTemp() + "," + d.getPressure() + \
    "," + d.getHumidity() + "," + d.getWind()+","


class Collector:
    def __init__(self, lat, lon, date):
        # Get your own API Key to use below vv
        self.apikey = "6485ec8a2eea6de7bde0c3f091d488e7"
        self.lat = lat
        self.lon = lon
        self.date = date

    # method to return climate data
    ''' Structure:
    - data from 15 days before landslide is at the front of the list. data for 5 days before landslide is at the end
    - order of the features is: precipitation, temperature, air pressure, humidity, and wind speed for each of the days
    Ex: [precip15, temp15, pressure15, humidity15, wind15, precip14, ... , humidity5, wind5]
    '''

    def getData(self):
        # get a list of dates from 5 to 15 days before event
        dates = self.gen_dates(self.lat, self.lon, self.date)
        # list containing weather data (precipitation, temperature, air pressure, humidity, then wind speed)
        weather = []

        # data is collected from 15, 14, 13 ... 5 days ago in that order (same order of the columns in the CSV)
        for date in dates:
            # parameters for the API call
            params = {'access_key': self.apikey, 'query': self.lat+","+self.lon, 'historical_date': date,
                      'hourly': '1', 'interval': '1'}
            api_result = requests.get(
                'https://api.weatherstack.com/historical', params)
            # API Response for current date and location
            api_response = api_result.json()

            # Use DataExtractor functions to get climate data.
            d = DataExtractor(api_response['historical'][date])
            weather.extend([d.getPrecip(), d.getTemp(),
                            d.getPressure(), d.getHumidity(), d.getWind()])
        return weather

    # returns list of dates from 15 days ago, then 14, 13, 12 ... 5
    def gen_dates(self, date, days_in_advance=15):
        date_list = []
        for i in range(5, days_in_advance + 1):
            temp_date = str(parser.parse(date) - datetime.timedelta(i))[:10]
            date_list.append(temp_date)
        date_list.reverse()
        return date_list

    def format_date(self, s):
        return s.replace("/", "-")

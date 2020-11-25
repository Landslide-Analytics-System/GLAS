import requests
import xml.dom.minidom
import os, sys
from time import sleep
import datetime
from dateutil import parser

class WeatherScraper:
	def __init__(self):
		self.api_format = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=cbdc0253c44449af88e45546202211&date='

	def format_date(self, s):
		return s.replace("/","-")
		
	# ObjectID, latitude, longitude, date, country, fatalities, injuries, type, trigger, severity, location
	def getInfo(self, entry):
		parts = entry.split(" ")
		return parts[0], parts[1], parts[2], format_date(parts[3][:10]), parts[5], parts[6], parts[7], parts[8], parts[9], parts[10], parts[11]

	# Return formatted list of API Parameters for the API call given the lat, lon, and date of the landslide.
	def gen_query(self, lat, lon, date, days_in_advance = 35):
		date_list = []
		params_list = []
		for i in range(days_in_advance + 1):
			temp_date = str(parser.parse(date) - datetime.timedelta(i))[:10]
			date_list.append(temp_date)
			params_list.append(temp_date+"&q="+lat+","+lon)
		return (date_list, params_list)

	# Return string containing info about the landslide
	def about(self, info):
		sen2 = ".\n There were " + info[5] + " fatalities and " + info[6] + " injuries.\n"
		sen3 = "This was a " + info[7] + " with " + info[9] + " severity near " + info[10] + " caused by " + info[8]
		return "Landslide occurred on " + info[3] + " at " + info[1] + ", " + info[2] + " in " + info[4] + sen2 + sen3

	# Get the data for each landslide
	def get_data(self):
		f = open("filtered_landslides.txt", "r")
		entries = f.readlines()

		f3 = open("finished.txt", "r")
		already_have = f3.read()

		# Go through landslides
		for i, landslide in enumerate(entries):
			oID, lat, lon, date, country, fatalities, injuries, l_type, trigger, severity, location = getInfo(landslide.strip())
			# Date is before 2008 or data has already been received for the landslide
			if (str(oID) + "..") in already_have or int(date[:4]) < 2008:
				print("Skip:",str(oID))
				continue

			print(oID, i, ": ", lat, lon, date)

			if not os.path.exists("Data/"+str(oID)):
				os.makedirs("Data/"+str(oID))

			# Generate formatted list of API parameters given lat, lon, and date.
			file_names, params = gen_query(lat, lon, date)

			for file_name, param in zip(file_names, params):
				api_call = self.api_format + param
				
				resp = requests.get(api_call)
				f_name = "Data/"+str(oID)+"/"+file_name+".xml"
				file = open(f_name, 'w+')
				file.write(str(resp.content))
				file.close()

			# Info about landslide
			f = open("Data/"+str(oID)+"/info.txt", "w+")
			f.write(about(getInfo(landslide.strip())))
			f.close()
			# Maintain Progress
			f2 = open("finished.txt", "a")
			f2.write(str(oID) + "..\n")
			f2.close()


import webbrowser 
import pandas as pd
import numpy as np

class LandslideScraper:

	def __init__(self):
		self.corner1 = [40, 62]
		self.corner2 = [-10, 150]

	def convert(self, field, func):
		self.df[field] = df[field].apply(func)

	def filter(self):
		self.df = df[(df.latitude >= corner2[0]) & (df.latitude <= corner1[0]) & (df.longitude >= corner1[1]) & (df.longitude <= corner2[1])]

	def writefile(self):
		f = open("filtered_landslides.txt", "w")
		for index, row in self.df.iterrows():
			f.write(str(row.OBJECTID)+" "+str(row.latitude)+" "+str(row.longitude)+" "+str(row.date)+" "+str(row.country)+" "+str(row.fatalities)+" "+str(row.injuries)+" "+str(row.type)+" "+str(row.trigger)+" "+str(row.severity)+" "+str(row.location)+"\n")
		f.close()
		print("\nGot:", len(df))

	def scrape(self):
		self.df = pd.read_csv("Global_Landslide_Catalog.csv")
		convert("latitude", float)
		convert("longitude", float)
		convert("fatalities", int)
		filter()

		writefile()


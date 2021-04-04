from bs4 import BeautifulSoup


class DataExtractor:
    # lid is the Landslide ID (folder name)
    # file_name is the file_name file name
    def __init__(self, lid, data):
        self.lid = lid
        self.extracted = False
        # self.file_name = file_name
        self.extracted = True
        self.data = str(data)

    def read(self):
        if self.extracted:
            return
        self.extracted = True
        file = open('Data/' + self.lid + "/" + self.file_name, 'r')
        self.data = file.read()

    # Return maximum precipitation in millimeters
    def maxPrecip(self):
        self.read()
        res = 0.0
        search = "<precipMM>"
        for i in range(len(self.data)):
            if self.data.startswith(search, i):
                res = max(res, float(
                    self.data[i + len(search):self.data.find("</precipMM", i)]))
        return str(res)

    # Return maximum temperature in Fahrenheit

    def maxTemp(self):
        self.read()
        res = 0.0
        search = "<HeatIndexF>"
        for i in range(len(self.data)):
            if self.data.startswith(search, i):
                res = max(res, float(
                    self.data[i + len(search):self.data.find("</HeatIndexF>", i)]))
        return str(res)

    # Return maximum air pressure

    def maxAirPressure(self):
        self.read()
        res = 0.0
        search = "<pressure>"
        for i in range(len(self.data)):
            if self.data.startswith(search, i):
                res = max(res, float(
                    self.data[i + len(search):self.data.find("</pressure>", i)]))
        return str(res)

    # Return maximum humidity

    def maxHumidity(self):
        self.read()
        res = 0.0
        search = "<humidity>"
        for i in range(len(self.data)):
            if self.data.startswith(search, i):
                res = max(res, float(
                    self.data[i + len(search):self.data.find("</humidity>", i)]))
        return str(res)

    # Return maximum wind speed in kilometers per hour

    def maxWind(self):
        self.read()
        res = 0.0
        search = "<windspeedKmph>"
        for i in range(len(self.data)):
            if self.data.startswith(search, i):
                res = max(res, float(
                    self.data[i + len(search):self.data.find("</windspeedKmph>", i)]))
        return str(res)

    def displayData(self):
        self.read()
        print(self.data)

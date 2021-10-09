class DataExtractor:
    # data is a json request from WeatherStack
    def __init__(self, data):
        self.data = data

    # return the maximum temperature
    def getTemp(self):
        return str(self.data['maxtemp'])

    # total rain in mm for the day
    def getPrecip(self):
        return str(self.getTot('precip'))

    # maximum humidity
    def getHumidity(self):
        return str(self.getMax('humidity'))

    # maximum wind speed
    def getWind(self):
        return str(self.getMax('wind_speed'))

    # maximum air pressure
    def getPressure(self):
        return str(self.getMax('pressure'))

    # var is a string feature.
    # returns the maximum value of var across all 25 hours
    def getMax(self, var):
        amt = 0
        for hour in self.data['hourly']:
            amt = max(amt, float(hour[var]))
        return amt

    # var is a string feature.
    # returns the average value of var across all 25 hours
    def getAvg(self, var):
        amt = 0
        for hour in self.data['hourly']:
            amt += float(hour[var])
        return amt / 24

    # var is a string feature.
    # returns the total value of var across all 25 hours
    def getTot(self, var):
        amt = 0
        for hour in self.data['hourly']:
            amt += float(hour[var])
        return amt

import csv
from datetime import time
from data_extractor import DataExtractor
import os
import datetime

class WeatherDataCompiler:
    def __init__(self):    
        self.csvfile = open('weather_data.csv', 'a')
        self.filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.filewriter.writerow(['id', 'date', 'lat', 'lon', 'country', 'fatalities', 'injuries', 'type', 'trigger', 'severity', 'location', 'precip35','temp35','air35','humidity35','wind35', 'precip34','temp34','air34','humidity34','wind34', 'precip33','temp33','air33','humidity33','wind33', 'precip32','temp32','air32','humidity32','wind32', 'precip31','temp31','air31','humidity31','wind31', 'precip30','temp30','air30','humidity30','wind30', 'precip29','temp29','air29','humidity29','wind29', 'precip28','temp28','air28','humidity28','wind28', 'precip27','temp27','air27','humidity27','wind27', 'precip26','temp26','air26','humidity26','wind26', 'precip25','temp25','air25','humidity25','wind25', 'precip24','temp24','air24','humidity24','wind24', 'precip23','temp23','air23','humidity23','wind23', 'precip22','temp22','air22','humidity22','wind22', 'precip21','temp21','air21','humidity21','wind21', 'precip20','temp20','air20','humidity20','wind20', 'precip19','temp19','air19','humidity19','wind19', 'precip18','temp18','air18','humidity18','wind18', 'precip17','temp17','air17','humidity17','wind17', 'precip16','temp16','air16','humidity16','wind16', 'precip15','temp15','air15','humidity15','wind15', 'precip14','temp14','air14','humidity14','wind14', 'precip13','temp13','air13','humidity13','wind13', 'precip12','temp12','air12','humidity12','wind12', 'precip11','temp11','air11','humidity11','wind11', 'precip10','temp10','air10','humidity10','wind10', 'precip9','temp9','air9','humidity9','wind9', 'precip8','temp8','air8','humidity8','wind8', 'precip7','temp7','air7','humidity7','wind7', 'precip6','temp6','air6','humidity6','wind6', 'precip5','temp5','air5','humidity5','wind5', 'precip4','temp4','air4','humidity4','wind4', 'precip3','temp3','air3','humidity3','wind3', 'precip2','temp2','air2','humidity2','wind2', 'precip1','temp1','air1','humidity1','wind1', 'precip0','temp0','air0','humidity0','wind0'])

    # Returns landslide date, lat, lon, country, fatalities, injuries, type, trigger, severity, and general location given the Landscape ID (folder name)
    def getInfo(self, lid):
        file = open("Data/" + lid + "/info.txt", "r")
        content = file.read()
        d_idx = content.find("on")
        date = content[d_idx + 3: d_idx + 13]
        l_idx = content.find("at")
        country = content[content.find(" in ") + 4: content.find("There") - 3]
        fatalities = content[content.find(" were ") + 6: content.find("fatalities") - 1]
        injuries = content[content.find(" and ") + 5: content.find("injuries") - 1]
        typet = content[content.find("This was a ") + 11: content.find("with") - 1]
        trigger = content[content.find("caused by") + 10:]
        severity = content[content.find(" with ") + 6: content.find("severity") - 1]
        location = content[content.find(" near ") + 6: content.find("caused by") - 1]
        return date, content[l_idx + 3: content.find("in") - 1].split(", ")[0], content[l_idx + 3: content.find("in") - 1].split(", ")[1],  country, fatalities, injuries, typet, trigger, severity, location
    
    def timeStats(self, total):
        end_time = datetime.datetime.now()
        print(round((end_time - total).total_seconds()*1000)/1000)

    def compile(self):
        f3 = open("wrote.txt", "r")
        already_have = int(f3.read())

        start_time = datetime.datetime.now()
        total = datetime.datetime.now()

        for i, (subdir, dirs, files) in enumerate(os.walk("Data")):
            if i == 0:
                continue
            oID = subdir[5:]
            if i <= already_have:
                continue
            weather = []
            files.sort()
            for file in files:
                if not file.endswith(".xml"):
                    continue
                d = DataExtractor(oID, file)
                weather.extend([d.maxPrecip(), d.maxTemp(), d.maxAirPressure(), d.maxHumidity(), d.maxWind()])
            
            info = self.getInfo(oID)
            
            content = [oID]
            content.extend(list(info))
            content.extend(weather)

            if not len(content) == 191:
                print("Issue with", oID,"  Length only", len(content))
                continue
            self.filewriter.writerow(content)

            f2 = open("wrote.txt", "w")
            f2.write(str(i))
            f2.close()

            if i % 30 == 0:
                print(i, " | ", oID, "     in  ", end = '')
                self.timeStats(total)

        self.csvfile.close()
        f3.close()

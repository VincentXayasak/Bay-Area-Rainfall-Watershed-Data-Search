import requests #pip install requests
import re
from watershed import Watershed

URL = 'https://alertdata.valleywater.org/Sensor/current'
HEADERS = {'accept': '*/*'}

class Search():
    """
    Class that searches for and inserts data into watershed objects.
    """

    def __init__(self):
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 200:
            data = (response.json())["precipitation"]
        else:
            raise requests.exceptions.HTTPError()

        #Needed to adjust time for daylight savings.
        self.date = re.search(r"[^T]+", data[0]["timestamp"]).group()
        self.time = re.search(r"\d+:\d+", data[0]["timestamp"]).group()
        if self.time[:2] == "23":
            self.time = self.time.replace(self.time[:2], "12", 1) + " am"
        elif int(self.time[:2]) >= 12:
            self.time = self.time.replace(self.time[:2], str(int(self.time[:2])-11), 1) + " pm"
        elif self.time[:2] == "11":
            self.time = self.time.replace(self.time[:2], "12", 1) + " pm"
        else:
            self.time = self.time.replace(self.time[:2], str(int(self.time[:2])+1), 1) + " am"

        self.watershedDict = {}
        for d in data:
            try:
                self.watershedDict[d["watershed"]].addData(**d)
            except KeyError:
                self.watershedDict[d["watershed"]] = Watershed(**d)
    
    def __repr__(self):
        return "\nBay Area Watershed Data Search As Of " + self.date + " " + self.time
        
    def getWatershedPrecipitation(self, watershedName, range):
        """
        Returns total amount of precipitation for a watershed in given range.
        """
        return self.watershedDict[watershedName].getTotalPrecipitation(range) 
    
    def getWatershedData(self, watershedName): 
        """
        Returns entire data of a watershed.
        """
        return self.watershedDict[watershedName].getEntireWatershedData() #Returns {Sensor:[1,3,6,12,24,YTD], Sensor:[1,3,6,12,24,YTD], ...}

    def rankPrecipitation(self, range):
        """
        Sorts each watershed depending on their precipitation amount during a given range.
        """
        precipitationDict = {}
        for watershed in self.watershedDict:
            precipitationDict[watershed] = (self.watershedDict[watershed].getTotalPrecipitation(range))
        return dict(sorted(precipitationDict.items(), key=lambda x:x[1], reverse=True)) #Returns {Watershed:Precipitation, Watershed:Precipitation, ...} sorted.
    
    def rankSensors(self, range):
        """
        Sorts each sensor depending on their precipitation amount during a given range.
        """
        sensorDict = {}
        for watershed in self.watershedDict:
            sensorDict.update(self.watershedDict[watershed].getEntireSensorData(range))
        return ((sensor, precipitation)  for sensor,precipitation in dict(sorted(sensorDict.items(), key=lambda x:x[1], reverse=True)).items()) #Returns generator that generates (Sensor, Precipitation) sorted.
    
    def getWatersheds(self):
        """
        Returns list of watershed names.
        """
        return self.watershedDict.keys()
class Watershed():
    """
    Class that hold all data of watersheds.
    """

    def __init__(self, **data):
        self.sensorDict = {}
        self.sensorDict[data["name"]] = [data["precip1Hr"],data["precip3Hr"],data["precip6Hr"],data["precip12Hr"],data["precip24Hr"],data["precipYtd"]]
    
    def addData(self, **data):
        """
        Adds more data into the dictionary containing all of the sensors' data for a watershed.
        """
        self.sensorDict[data["name"]] = [data["precip1Hr"],data["precip3Hr"],data["precip6Hr"],data["precip12Hr"],data["precip24Hr"],data["precipYtd"]]
    
    def getTotalPrecipitation(self, range):
        """
        Calculates total precipitation of a watershed during a time period.
        """
        allPrecipitation = []
        for l in self.sensorDict.values():
            allPrecipitation.append(l[range-1])
        return round(sum(allPrecipitation), 2)

    def getEntireWatershedData(self):
        """
        Returns the entire data of a watershed.
        """
        return self.sensorDict
    
    def getEntireSensorData(self, range):
        """
        Returns all sensors and its data of watershed during a time period. 
        """
        sensorPrecipitation = {}
        for sensor, data in self.sensorDict.items():
            sensorPrecipitation[sensor] = data[range-1]
        return sensorPrecipitation #Returns {Sensor:Precipitation, Sensor:Precipitation, ...}
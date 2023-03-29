import requests
from search import Search

class UI:
    """
    Class that interacts with user.
    """

    def __init__(self):
        try:
            self.search = Search()
        except requests.exceptions.HTTPError:
            raise SystemExit("Status Unavailable Right Now.")
        print(self.search)

        wsList = list(self.search.getWatersheds())
        print("Watersheds: "+", ".join(wsList))
        self.watershedLookup = {}
        for i in range(len(wsList)):
            self.watershedLookup[i+1] = wsList[i]
        self.rangeLookup = {1:"1 Hour Ago", 2:"3 Hours Ago", 3:"6 Hours Ago", 4:"12 Hours Ago", 5:"24 Hours Ago", 6:"Year To Date"}

    def displayWatershedPrecipitation(self):
        """
        Displays total watershed precipitation of a watershed during given range.
        """
        print()
        for num, ws in self.watershedLookup.items():
            print(str(num)+". "+ws)
        inp = 0
        while not 1 <= inp <= len(self.watershedLookup):
            try: 
                inp = int(input("\nWhich Watershed Do You Need Precipitation Data From? (1-"+str(len(self.watershedLookup))+"): "))
                if not 1 <= inp <= len(self.watershedLookup):
                    raise ValueError
            except ValueError:
                print("Error!", end=" ")
        watershedName = self.watershedLookup[inp]
        
        print()
        for num, range in self.rangeLookup.items():
            print(str(num)+". "+range)
        range = 0
        while not 1 <= range <= 6:
            try:
                range = int(input("\nRange (1-6): "))
                if not 1 <= range <= 6:
                    raise ValueError
            except ValueError:
                print("Error!", end=" ")
        print("\n" + watershedName + " Has Had A Total Precipitation Of",self.search.getWatershedPrecipitation(watershedName, range),"Inches From "+self.rangeLookup[range]+".")
    
    def displayWatershedData(self):
        """
        Displays entire data for a watershed.
        """
        print()
        for num, ws in self.watershedLookup.items():
            print(str(num)+". "+ws)
        inp = 0
        while not 1 <= inp <= len(self.watershedLookup):
            try: 
                inp = int(input("\nFull Data From Which Watershed? (1-"+str(len(self.watershedLookup))+"): "))
                if not 1 <= inp <= len(self.watershedLookup):
                    raise ValueError
            except ValueError:
                print("Error!", end=" ")
        watershedName = self.watershedLookup[inp]
        print("\n"+watershedName + " Data:")
        print("Precipitation (Inches)" + (" "*13) + "1 Hr" + (" "*2) + "3 Hr" + (" "*2) + "6 Hr" + (" "*2) + "12 Hr" + " 24 Hr" + (" "*2) + "YTD\n")
        for sensor, dataList in self.search.getWatershedData(watershedName).items():
            spacing1 = 35 - len(sensor)
            print(sensor, end = (" "*spacing1))
            for p in dataList:
                spacing2 = 6 - len(str(p))
                print(p, end = (" "*spacing2))
            print("\n")
    
    def displayRankedWatersheds(self):
        """
        Displays watersheds ranked by amount of precipitation during given range.
        """
        print()
        for num, range in self.rangeLookup.items():
            print(str(num)+". "+range)
        range = 0
        while not 1 <= range <= 6:
            try:
                range = int(input("\nRange (1-6): "))
                if not 1 <= range <= 6:
                    raise ValueError
            except ValueError:
                print("Error!", end=" ")
        print("\nPrecipitation (Inches) From " + self.rangeLookup[range] + ":\n")
        count = 1
        for watershed, precipitation in self.search.rankPrecipitation(range).items():
            spacing = 20 - len(watershed)
            print(str(count) + ". " + watershed + (" "*spacing) + str(precipitation) + "\n")
            count += 1
    
    def displayRankedSensors(self):
        """
        Displays each sensor one by one ranked by amount of precipitation during a given range.
        """
        print()
        for num, range in self.rangeLookup.items():
            print(str(num)+". "+range)
        range = 0
        while not 1 <= range <= 6:
            try:
                range = int(input("\nRange (1-6): "))
                if not 1 <= range <= 6:
                    raise ValueError
            except ValueError:
                print("Error!", end=" ")
        rankedGenerator = self.search.rankSensors(range)
        count = 1
        print("\nSensors' Precipitation (Inches) Ranked From " + self.rangeLookup[range] + ":\n")
        print("Click Enter Key To Keep Displaying Sensors\n")
        inp = ""
        while inp == "":
            try:
                sensor, precipitation = next(rankedGenerator)
            except StopIteration:
                print("No More Sensors\n")
                break
            if not count >= 10:
                spacing = 35 - len(sensor)
            else:
                spacing = 34 - len(sensor)
            print(str(count) + ". " + sensor + (" "*spacing) + str(precipitation))
            count += 1
            inp = input()
        
    def run(self):
        """
        Displays menu and calls functions.
        """
        menu = {"1":self.displayWatershedPrecipitation, "2":self.displayWatershedData, "3":self.displayRankedWatersheds, "4":self.displayRankedSensors}
        print("\nMenu:\n1. Find Precipitation For A Watershed During A Time Period\n2. Find All Data For A Watershed\n3. Display Watersheds Ranked During A Time Period\n4. Display Sensors Ranked During A Time Period\n5. Quit\n")
        inp = input("Enter Choice: ")
        while inp != "5":
            try:
                menu[inp]()
            except KeyError:
                print("\nError!")
            print("\nMenu:\n1. Find Precipitation For A Watershed During A Time Period\n2. Find All Data For A Watershed\n3. Display Watersheds Ranked During A Time Period\n4. Display Sensors Ranked During A Time Period\n5. Quit\n")
            inp = input("Enter Choice: ")

UI().run()
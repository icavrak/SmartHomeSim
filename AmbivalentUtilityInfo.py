from UtilityInfo import UtilityInfo

class AmbivalentUtilityInfo(UtilityInfo):


    def startUtility(self, time):
        return float(1)


    def getDescription(self):
        return "Default ambivalent utility, returns 1.0 whenever it is scheduled to start"
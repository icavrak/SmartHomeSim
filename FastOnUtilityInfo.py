from UtilityInfo import UtilityInfo

class FastOnUtilityInfo(UtilityInfo):


    __current_time = None
    __timeOn = None

    #constructor,
    # currentTime - current simulation time (datetime)
    # timeOn - time limit for turning the device on (utiliy drops to 0 after that period) (timedelta)
    def __init__(self, currentTime, timeOn):
        self.__current_time = currentTime
        self.__timeOn = timeOn

    def startUtility(self, time):
        if time - self.__current_time > self.__timeOn:
            return float(0)
        else:
            return float(1)


    def getDescription(self):
        return "FastOn utility, returns 1.0 if within short time period from the On request, 0 otherwise"
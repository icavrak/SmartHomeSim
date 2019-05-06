class SimulationEvent:


    def __init__(self, simtime, target=None):

        self.__time = simtime
        self.__target = target
        self.__active = True


    def trigger(self):
        if self.__target != None:
            self.__target(self)

    def __cmp__(self, other):
        return cmp(self.__time, other.__time)

    def getTimestamp(self):
        return self.__time

    def setTimestamp(self, timestamp):
        self.__time = timestamp

    def getTarget(self):
        return self.__target

    def isActive(self):
        return self.__active

    def invalidate(self):
        self.__active = False

from abc import abstractmethod

class UtilityInfo:

    def getUtilityAtTime(self, time, duration):
        total_utility = self.startUtility(time) + self.endUtility(time) + self.activityUtility(time, duration)
        if total_utility > 1.0:
            raise Exception("Utility error: value larger than 1.0 (start=" + str(self.startUtility(time)) + ", end=" + str(self.endUtility(time)) + ", activity=" + str(self.activityUtility(time, duration)) + ".")
        else:
            return total_utility

    def startUtility(self, time):
        return float(0)

    def endUtility(self, time):
        return float(0)

    def activityUtility(self, time, duration):
        return float(0)

    @abstractmethod
    def getDescription(self):
        pass

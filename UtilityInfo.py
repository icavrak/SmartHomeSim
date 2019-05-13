from abc import abstractmethod
from datetime import datetime
from datetime import timedelta

class UtilityInfo:

    def getUtilityAtTime(self, startTime, duration):
        assert(isinstance(startTime, datetime))
        assert(isinstance(duration, timedelta))

        total_utility = self.startUtility(startTime) + self.endUtility(startTime + duration) + self.activityUtility(startTime, duration)
        return total_utility

        #if total_utility > 1.0:
        #    raise Exception("Utility error: value larger than 1.0 (start=" + str(self.startUtility(time)) + ", end=" + str(self.endUtility(time)) + ", activity=" + str(self.activityUtility(time, duration)) + ".")
        #else:
         #   return total_utility

    def startUtility(self, time):
        return float(0)

    def endUtility(self, time):
        return float(0)

    def activityUtility(self, time, duration):
        return float(0)

    @abstractmethod
    def getDescription(self):
        pass

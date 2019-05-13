from UtilityInfo import UtilityInfo
from datetime import datetime
from datetime import time


class RestrictedOffUtilityInfo(UtilityInfo):


    __current_time = None
    __restrictedTimeStart = None
    __restrictedTimeEnd = None

    #constructor,
    # restrictedStart - start of restricted time in a day (type datetime.time)
    # restrictedEnd - end of restricted time in a day (type datetime.time)
    def __init__(self, restrictedStart, restrictedEnd):

        #check data types (must be datetime.time)
        assert(isinstance(restrictedStart, time))
        assert(isinstance(restrictedEnd, time))

        self.__restrictedTimeStart = restrictedStart
        self.__restrictedTimeEnd = restrictedEnd


    def endUtility(self, end_time):

        assert(isinstance(end_time, datetime))

        curr_time = end_time.time()

        if self.__restrictedTimeStart < self.__restrictedTimeEnd:
            if (curr_time > self.__restrictedTimeStart) and (curr_time < self.__restrictedTimeEnd):
                return float(0)
            else:
                return float(1)

        else:
            if (curr_time > self.__restrictedTimeEnd) and (curr_time < self.__restrictedTimeStart):
                return float(1)
            else:
                return float(0)

    def getDescription(self):
        return "RestrictedOff utility, returns 1.0 if device ends activity within allowed end time span, 0 otherwise"
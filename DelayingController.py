from ControllerDevice import ControllerDevice
from DeviceOnRequestEvent import DeviceOnRequestEvent
from DeviceOnEvent import DeviceOnEvent
from simulator import SmartHomeSim, EventScheduler
from PriceInfo import PriceInfo
from datetime import timedelta
from ManagedDevice import ManagedDevice
from UtilityInfo import UtilityInfo
from AmbivalentUtilityInfo import AmbivalentUtilityInfo

import simhelper

class DelayingController(ControllerDevice):

    __initialized = None
    __defaultUtilityInfo = AmbivalentUtilityInfo()

    __max_price = 1.0
    __min_price = 10000.0

    def __init__(self):
        __initialized = False

    def __init__(self, init):
        __initialized = True

    def getDescription(self):
        return "Delaying controller device >" + self.name + "< (single Controller device permitted in the system\nController device must be named '#controller'"

    def onRequest(self, event):

        #get Simulation Context and Event Scheduler objects
        simContext = self.getSimulationContext()

        #get the pricing information object
        price_info = simContext.getPriceInfo()

        #get utility info object from the request
        utilityInfo = event.getTargetDevice().getUtilityInfo()

        #get current time
        current_time = simContext.getSimCurrentTime()

        #if there is no utilityInfo attached to the event, use the default one
        if utilityInfo == None:
            utilityInfo = self.__defaultUtilityInfo

        #create new deviceON event with the same activation time as requested
        res_event = DeviceOnEvent(event.getCurrentTime(), event.getTargetDevice())

        #check for start delay if the target device is ManagedDevice
        if isinstance(event.getTargetDevice(), ManagedDevice):

            #get the current price
            current_utility = utilityInfo.getUtilityAtTime(current_time, event.getEstimatedDuration())
            current_price = price_info.getCurrentPrice()

            #record minimal and maximal prices
            self.__max_price = max(current_price, self.__max_price)
            self.__min_price = min(current_price, self.__min_price)

            #check if the future pricing within the allowed start delay period is lower
            #at some point in time (determine the nearest point in time) using the timestep
            # of 10 minutes
            #within the allowed delay determined by price horizon (allowed delay in minutes)
            inspection_period = timedelta(hours=price_info.getPriceHorizon())
            inspection_step = timedelta(minutes=10)

            #calculate prices and utility for the price horizon
            start_period = 0
            current_utility_price = current_utility / current_price
            future_price = []
            future_utility = []
            future_utility_price = []
            while inspection_step * start_period < inspection_period:

                future_price.append(price_info.getPriceAtTime(current_time + inspection_step * start_period))
                future_utility.append(utilityInfo.getUtilityAtTime(current_time + inspection_step * start_period, event.getEstimatedDuration()))
                future_utility_price.append(future_utility[start_period] / future_price[start_period])
                start_period = start_period + 1

            #find the first more convenient time to allow deviceON event...
            start_period = 0
            while inspection_step * start_period < inspection_period:
                #if future_utility_price[start_period] > current_utility_price:
                if future_utility[start_period] < 0.8:
                    break
                else:
                    start_period = start_period + 1

            #if there is such moment, delay the start
            if inspection_step * start_period < inspection_period:
                res_event = DeviceOnEvent(event.getCurrentTime() + (start_period*inspection_step).seconds, event.getTargetDevice())

        #add event to the event queue
        try:
            simContext.addSimEvent(res_event)
        except:
            pass  # end of simulation


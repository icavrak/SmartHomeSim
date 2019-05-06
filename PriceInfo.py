from datetime import datetime
from datetime import timedelta


class PriceInfo:

    __simulation        = None
    __pricing_profile   = None

    def __init__(self, simulation, pricing_profile):

        self.__simulation        = simulation
        self.__pricing_profile   = pricing_profile


    #get current price
    def getCurrentPrice(self):
        return self.__simulation.getCurrentPrice()

    #price horizon - how far in advance pricing data can be acquired (in hours)
    def getPriceHorizon(self):
        return self.__simulation.getPriceHorizon()


    #returns an array of prices, each element of an array is a price at the
    #beginning of a corresponding timeslot lasting "time_step" minutes, for
    #"steps" periods ( arguments 10, 12 -> 10-minute periods, 12 periods =
    # 120 minutes ahead of the current simulation time
    # None if the time_step*steps exceeds price horizon
    def getPricingForPeriod(self, time_step, steps):

        #check that all the period fits into the price horizon
        if time_step*steps > self.getPriceHorizon() * 60:
            return None

        #prepare the array
        price_array = []

        #iterate over all periods and collect pricing data
        for slot in range(0, steps):
            price_array.append(self.getPriceFromNow(timedelta(minutes=slot*time_step)))

        #return the filled array
        return price_array


    # get price at absolute time t (t is datetime type)
    # None if the specified time is not within the price horizon
    def getPriceAtTime(self, time):

        #check that the requested time is within the price horizon
        if time > self.__simulation.getSimCurrentTime() + timedelta(hours=self.getPriceHorizon()):
            return None

        #return the price for the requested time
        return self.__pricing_profile.getCurrentPrice(time)



    # get price at t from current simulation time (t is timedelta type)
    # None if the specified timedelta is not within the price horizon
    def getPriceFromNow(self, timedelta):

        #calculate the absoulute time
        absolute_time = self.__simulation.getSimCurrentTime() + timedelta

        #return the price for the requested time
        return self.getPriceAtTime(absolute_time)



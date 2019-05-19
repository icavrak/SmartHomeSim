from UtilityInfo import UtilityInfo
from datetime import datetime
from datetime import time
from datetime import timedelta
from Device import Device

class CummulativeUtilityInfo(UtilityInfo):


    __current_time  = None

    __lossF         = None
    __targetF       = None
    __utilF         = None

    __device        = None

    #constructor,
    # restrictedStart - start of restricted time in a day (type datetime.time)
    # restrictedEnd - end of restricted time in a day (type datetime.time)
    def __init__(self, device):

        #check that appropriate device type was supplied
        assert(isinstance(device, Device))

        self.__device = device

    def setLossFunction(self, lossF):
        self.__lossF = lossF

    def setTargetFunction(self, targetF):
        self.__targetF = targetF

    def setUtilityFunction(self, utilF):
        self.__utilF = utilF


    def activityUtility(self, time, duration):

        assert (self.__lossF != None)
        assert (self.__targetF != None)
        assert (self.__utilF != None)

        #get current temperature
        current_temp = self.__device.getCurrentTemperature()

        #in steps of 60 seconds, calculate temperature loss
        timestep = 600
        accumulated_temperature_loss = 0
        accumulated_temperature_loss_delta = 0
        accumulated_temperature_gain = 0

        #calculate temperature loss prior to heater activation
        current_time = self.__device.getSimulationContext().getSimCurrentTime()
        while current_time < (time + duration):
            accumulated_temperature_loss += self.__device.calculateTemperatureLoss(current_time, timestep)
            current_time += timedelta(seconds=timestep)

        # calculate temperature loss during heater activation
        current_time = time
        while current_time < (time + duration):
            accumulated_temperature_loss_delta += self.__device.calculateTemperatureLoss(current_time, timestep)
            current_time += timedelta(seconds=timestep)

        #calculate temperature gain during heater activation
        accumulated_temperature_gain = self.__device.calculateTemperatureGain(time, duration.seconds)

        temperature_start_period = current_temp - accumulated_temperature_loss
        temperature_end_period = current_temp - accumulated_temperature_loss - accumulated_temperature_loss_delta + accumulated_temperature_gain

        util_start_period = self.__utilF(temperature_start_period, time, self.__targetF)
        util_end_period = self.__utilF(temperature_end_period, time, self.__targetF)

        return min(util_start_period, util_end_period)

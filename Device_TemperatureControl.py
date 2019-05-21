from ManagedDevice import ManagedDevice
from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from datetime import timedelta
from datetime import datetime
import simhelper
from CummulativeUtilityInfo import CummulativeUtilityInfo

class Device_TemperatureControl(ManagedDevice):

    def __init__(self):

        self.__heat_power = 0
        self.__loss_coefficient = 0
        self.__heat_coefficient = 0

        self.__loss_function = None
        self.__target_function = None
        self.__utility_function = None

        self.__on_point = 0
        self.__off_point = 0

        self.__last_time = 0
        self.__last_temperature_delta = 0

        self.__current_temperature = 0
        self.__on = False

        self.__onRequestPending = False


    def __init__(self, init):
        init_a = init.split(",")

        # heating power in Watts
        self.__heat_power = float(init_a[0])

        #loss coefficient
        self.__loss_coefficient = float(init_a[1])

        #heating coefficient
        self.__heat_coefficient = float(init_a[2])

        #on point
        self.__on_point = float(init_a[3])

        # off point
        self.__off_point = float(init_a[4])

        #last time the device was polled for power (used for calculating time delta)
        self.__last_time = 0

        #temperature at simulation start
        self.__current_temperature = float(init_a[5])

        self.__last_temperature_delta = 0

        self.__on = False

        self.__onRequestPending = False

    def getDescription(self):
        return "TemperatureControl device >" + self.getDeviceName() + "< with heating consumption " + self.self.__heat_power + "W."


    def deviceSimInit(self):

        #register additional columns in the log file
        if self.getSimulationContext().getSimLogger() != None:
            self.getSimulationContext().getSimLogger().registerVariable(self.getDeviceName() + "_temp")         #current temp
            self.getSimulationContext().getSimLogger().registerVariable(self.getDeviceName() + "_target")       #target temp
            self.getSimulationContext().getSimLogger().registerVariable(self.getDeviceName() + "_loss")         #heat loss
            self.getSimulationContext().getSimLogger().registerVariable(self.getDeviceName() + "_utility")      #utility


    def getCurrentConsumption(self, time):

        assert( isinstance(time, datetime))

        #calculate time delta (in seconds)
        if self.__last_time != 0:
            delta = (time - self.__last_time).seconds
        else:
            delta = 0
        self.__last_time = time

        #calculate temperature loss per second
        #loss = (max(self.__current_temperature - self.__loss_function(self.__current_temperature, time), 0.0) * self.__loss_coefficient)
        #loss = self.__loss_function(self.__current_temperature, time) * self.__loss_coefficient
        #loss = loss * delta / 3600.0
        loss = self.calculateTemperatureLoss(time, delta)

        #calculate temperature gain per second
        if self.__on:
            #gain = (self.__heat_power / 1000.0) * self.__heat_coefficient
            #gain = gain * delta / 3600.0
            gain = self.calculateTemperatureGain(time, delta)
        else:
            gain = 0.0


        #calculate resulting temperature
        ponder_coefficient = 0.1
        self.__last_temperature_delta = (self.__last_temperature_delta * ponder_coefficient) + (1.0 - ponder_coefficient) * (gain - loss)
        self.__current_temperature = self.__current_temperature + self.__last_temperature_delta


        #log current device values
        self.getSimulationContext().getSimLogger().logVariable(self.getDeviceName() + "_temp", self.__current_temperature)
        self.getSimulationContext().getSimLogger().logVariable(self.getDeviceName() + "_target", self.__target_function(self.__current_temperature, time))
        self.getSimulationContext().getSimLogger().logVariable(self.getDeviceName() + "_loss", self.__loss_function(self.__current_temperature, time))
        self.getSimulationContext().getSimLogger().logVariable(self.getDeviceName() + "_utility", self.getCurrentUtility(time))

        #self.__utility_function(self.__current_temperature, time, self.__target_function))


        #determine current heating power and report it
        power = 0.0

        if self.__on == True:
            power = self.__heat_power


        #is off set-point reached?
        if self.__current_temperature >= self.__target_function(self.__current_temperature, time) + self.__off_point:
            #self.off()
            simContext = self.getSimulationContext()
            simEventScheduler = simContext.getSimEventScheduler()
            off_event = DeviceOffRequestEvent(0, self)
            simEventScheduler.oneshotRelativeToNow(timedelta(seconds=0), off_event)

        #is on set-point reached?
        if self.__current_temperature <= self.__target_function(self.__current_temperature, time) - self.__on_point:
            #self.on()
            simContext = self.getSimulationContext()
            simEventScheduler = simContext.getSimEventScheduler()
            gain = (self.__heat_power / 1000.0) * self.__heat_coefficient * delta / 3600.0
            if not gain == 0.0 and self.__onRequestPending == False:
                estimated_time = timedelta(seconds=( self.__target_function(self.__current_temperature, time) - self.__current_temperature)  / gain)
                on_event = DeviceOnRequestEvent(simhelper.create_timestamp(simContext.getSimCurrentTime()), self, estimated_time)
                simEventScheduler.oneshotRelativeToNow(timedelta(seconds=0), on_event)
                self.__onRequestPending = True

        #return current power consumption (valid for last time delta period)
        return power

    #get device current utility
    def getCurrentUtility(self, time):

        assert (isinstance(time, datetime))

        return self.__utility_function(self.__current_temperature, time, self.__target_function)


    def on(self):
        self.__on = True

        self.__onRequestPending = False

        # get simulation context and event scheduler
        simContext = self.getSimulationContext()
        simEventScheduler = simContext.getSimEventScheduler()

        # schedule the "off" event after the __on_duration seconds of activity
        off_event = DeviceOffRequestEvent(0, self)

        # post the off request event
        #simEventScheduler.oneshotRelativeToNow(self.__on_duration, off_event)


    def off(self):
        self.__on = False


    def setLossFunction(self, lossFunction):
        self.__loss_function = lossFunction

    def setTargetFunction(self, targetFunction):
        self.__target_function = targetFunction

    def setUtilityFunction(self, utilityFunction):
        self.__utility_function = utilityFunction

    def setOnPoint(self, on_point):
        self.__on_point = on_point

    def setOffPoint(self, off_point):
        self.__off_point = off_point

    def getOnPoint(self):
        return self.__on_point

    def getOffPoint(self):
        return self.__off_point

    def getCurrentTemperature(self):
        return self.__current_temperature

    def calculateTemperatureLoss(self, time, delta):
        assert( isinstance(time, datetime) )
        assert( isinstance(delta, int) )
        loss = self.__loss_function(self.__current_temperature, time) * self.__loss_coefficient
        loss = loss * delta / 3600.0
        return loss

    def calculateTemperatureGain(self, time, delta):
        assert( isinstance(time, datetime) )
        assert( isinstance(delta, int) )
        gain = (self.__heat_power / 1000.0) * self.__heat_coefficient
        gain = gain * delta / 3600.0
        return gain
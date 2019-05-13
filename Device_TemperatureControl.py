from ManagedDevice import ManagedDevice
from DeviceOffRequestEvent import DeviceOffRequestEvent
from datetime import timedelta

class Device_TemperatureControl(ManagedDevice):

    def __init__(self):
        self.__loss_function = None
        self.__loss_coefficient = 0
        self.__heat_coefficient = 0
        self.__heat_power = 0
        self.__target_function = None
        self.__utility_function = None
        self.__on = False

    def __init__(self, init):
        init_a = init.split(",")

        # current consumption in Watts
        self.current_consumption = float(init_a[0])

        # fixed period the device is turned on, then turned back off
        self.__on_duration = timedelta(seconds=int(init_a[1]))

        self.__on = False

    def getDescription(self):
        return "Delayable device >" + self.getDeviceName() + "< with constant consumption " + self.current_consumption + "W."


    def deviceSimInit(self):

        #register additional column in the log file
        if self.getSimulationContext().getSimLogger() != None:
            self.getSimulationContext().getSimLogger().registerVariable(self.getDeviceName() + "_temp")

    def getCurrentConsumption(self, time):

        if self.__on == True:
            return self.current_consumption
        else:
            return 0

    def on(self):
        self.__on = True

        # get simulation context and event scheduler
        simContext = self.getSimulationContext()
        simEventScheduler = simContext.getSimEventScheduler()

        # schedule the "off" event after the __on_duration seconds of activity
        off_event = DeviceOffRequestEvent(0, self)

        # post the off request event
        simEventScheduler.oneshotRelativeToNow(self.__on_duration, off_event)


    def off(self):
        self.__on = False

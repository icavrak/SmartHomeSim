from UnmanagedDevice import UnmanagedDevice
from DeviceOffRequestEvent import DeviceOffRequestEvent
from datetime import timedelta

import simhelper

class Device_OnOff_Timed(UnmanagedDevice):

    __on_duration = 0

    def __init__(self):
        self.current_consumption = 0
        self.__on_duration = 0
        self.__on = False

    def __init__(self, init):

        init_a = init.split(",")

        #current consumption in Watts
        self.current_consumption = float(init_a[0])

        #fixed period the device is turned on, then turned back off
        self.__on_duration = int(init_a[1])

        self.__on = False

    def getDescription(self):
        return "Generic ON/OFF device >" + self.name + "< with constant consumption " + self.current_consumption + "W and fixed on period " + self.__on_duration + "s."

    def getCurrentConsumption(self, time):

        if self.__on == True:
            return self.current_consumption
        else:
            return 0

    def on(self):
        self.__on = True

        #get simulation context and event scheduler
        simContext = self.getSimulationContext()
        simEventScheduler = simContext.getSimEventScheduler()

        #schedule the "off" event after the __on_duration seconds of activity
        off_event = DeviceOffRequestEvent(0, self)

        #post the off request event
        simEventScheduler.oneshotRelativeToNow(timedelta(seconds=self.__on_duration), off_event)


    def off(self):
        self.__on = False

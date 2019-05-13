from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from PriceInfo import PriceInfo
from datetime import timedelta
from datetime import time
from FastOnUtilityInfo import FastOnUtilityInfo
from RestrictedOffUtilityInfo import RestrictedOffUtilityInfo


class Device_Scheduler_4(SpecialPurposeDevice):

    initialized = None

    def __init__(self):
        initialized = False

    def __init__(self, init):
        initialized = True

    def getDescription(self):
        return "Scheduler device >" + self.name + "<"


    def onNewDate(self):

        #get the simulation context object
        simContext = self.getSimulationContext()

        #get the scheduler helper object from the context
        simEventScheduler = simContext.getSimEventScheduler()

        #set utilities for devices (UtiliyInfo descendant classes implementing utiliy profiles
        #of devices (if not set, default utiliy for a device is AmbivalentUtilityInfo)
        tv_utility = FastOnUtilityInfo(simContext.getSimCurrentTime(), timedelta(seconds=1))
        simContext.getDevice("tv").setUtilityInfo(tv_utility)

        heater_utility = RestrictedOffUtilityInfo(time(0, 0), time(9, 0))
        simContext.getDevice("grijalica").setUtilityInfo(heater_utility)

        ##########################
        #
        # TV scheduled "on" event
        #
        ##########################
        tv_duration = timedelta(hours=4)
        event2_on = DeviceOnRequestEvent(0, simContext.getDevice("tv"), tv_duration, 25.0)
        event2_off = DeviceOffRequestEvent(0, simContext.getDevice("tv"))

        # post the "on" event for device2 to the event queue (lasts 3 hours)
        simEventScheduler.oneshotToday(time(20, 0), event2_on)
        simEventScheduler.oneshotRelativeToEvent(event2_on, tv_duration, event2_off)


        ##########################
        #
        #   heater on event
        #
        ##########################
        event4 = DeviceOnRequestEvent(0, simContext.getDevice("grijalica"), timedelta(hours=3), 30.0)

        # post the "on" event for device4 to the event queue
        simEventScheduler.oneshotToday(time(20, 0), event4)
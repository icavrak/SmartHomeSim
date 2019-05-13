from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from PriceInfo import PriceInfo
from datetime import timedelta
from datetime import time
from FastOnUtilityInfo import FastOnUtilityInfo
from RestrictedOffUtilityInfo import RestrictedOffUtilityInfo


class Device_Scheduler_3(SpecialPurposeDevice):

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

        dishwasher_utility = RestrictedOffUtilityInfo(time(6,0), time(9,0))
        simContext.getDevice("sudjerica").setUtilityInfo(dishwasher_utility)

        laundry_utility = RestrictedOffUtilityInfo(time(0, 0), time(9, 0))
        simContext.getDevice("vesmasina").setUtilityInfo(laundry_utility)

        # scheduled "on" event for device1
        event1_on = DeviceOnRequestEvent(0, simContext.getDevice("stednjak"))
        event1_off = DeviceOffRequestEvent(0, simContext.getDevice("stednjak"))


        # TV scheduled "on" event
        tv_duration = timedelta(hours=4)
        event2_on = DeviceOnRequestEvent(0, simContext.getDevice("tv"), tv_duration, 25.0)
        event2_off = DeviceOffRequestEvent(0, simContext.getDevice("tv"))

        #on weekdays ...
        if simContext.isWeekday():

            #post the "on" event for device1 to the event queue
            #device has no start delay tolerance and expected on period is 1 hour
            simEventScheduler.oneshotToday(time(17,30), event1_on)
            simEventScheduler.oneshotRelativeToEvent(event1_on, timedelta(hours=1), event1_off)

            # post the "on" event for device2 to the event queue (lasts 3 hours)
            simEventScheduler.oneshotToday(time(20,0), event2_on)
            simEventScheduler.oneshotRelativeToEvent(event2_on, tv_duration, event2_off)

        else:

            # post the "on" event for device1 to the event queue
            # device has no start delay tolerance and expected on period is 2 hours
            simEventScheduler.oneshotToday(time(11, 0), event1_on)
            simEventScheduler.oneshotRelativeToEvent(event1_on, timedelta(hours=2), event1_off)

            # post the "on" event for device1 to the event queue, on for 5 hours
            simEventScheduler.oneshotToday(time(20, 0), event2_on)
            simEventScheduler.oneshotRelativeToEvent(event2_on, timedelta(hours=4), event2_off)



        # device3 scheduled "on" event, has estimated duration of 2 hours (120mins),
        # device has expected consumption of 20W, and should not end between 06am and 09am hours
        event3 = DeviceOnRequestEvent(0, simContext.getDevice("sudjerica"), timedelta(hours=2), 25.0)

        # post the "on" event for device3 to the event queue
        #simEventScheduler.oneshotToday(time(20, 0), event3)

        # device4 scheduled "on" event, has estimated duration of 3 hours,
        # device has expected consumption of 30W, and should not end between 23am and 09am hours

        event4 = DeviceOnRequestEvent(0, simContext.getDevice("vesmasina"), timedelta(hours=3), 30.0)

        # post the "on" event for device3 to the event queue
        simEventScheduler.oneshotToday(time(20, 0), event4)
from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from PriceInfo import PriceInfo
from datetime import timedelta
from datetime import time


class Device_Scheduler_2(SpecialPurposeDevice):

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



        # scheduled "on" event for device1
        event1_on = DeviceOnRequestEvent(0, simContext.getDevice("stednjak"))
        event1_off = DeviceOffRequestEvent(0, simContext.getDevice("stednjak"))


        # device2 scheduled "on" event
        event2_on = DeviceOnRequestEvent(0, simContext.getDevice("tv"))
        event2_off = DeviceOffRequestEvent(0, simContext.getDevice("tv"))

        #on weekdays ...
        if simContext.isWeekday():

            #post the "on" event for device1 to the event queue
            #device has no start delay tolerance and expected on period is 1 hour
            simEventScheduler.oneshotToday(time(17,30), event1_on)
            simEventScheduler.oneshotRelativeToEvent(event1_on, timedelta(seconds=3600), event1_off)

            # post the "on" event for device2 to the event queue (lasts 3 hours)
            simEventScheduler.oneshotToday(time(19, 0), event2_on)
            simEventScheduler.oneshotRelativeToEvent(event2_on, timedelta(seconds=10800), event2_off)

        else:

            # post the "on" event for device1 to the event queue
            # device has no start delay tolerance and expected on period is 2 hours
            simEventScheduler.oneshotToday(time(11, 0), event1_on)
            simEventScheduler.oneshotRelativeToEvent(event1_on, timedelta(seconds=7200), event1_off)

            # post the "on" event for device1 to the event queue, on for 5 hours
            simEventScheduler.oneshotToday(time(18, 0), event2_on)
            simEventScheduler.oneshotRelativeToEvent(event2_on, timedelta(seconds=18000), event2_off)



        # device3 scheduled "on" event, has estimated duration of 2 hours (120mins),
        # device has expected consumption of 20W, and is ambivalent to start, duration and end times
        event3 = DeviceOnRequestEvent(0, simContext.getDevice("sudjerica"), timedelta(minutes=120), 20.0)

        # post the "on" event for device3 to the event queue
        simEventScheduler.oneshotToday(time(20, 0), event3)


from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from PriceInfo import PriceInfo
from datetime import timedelta


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
            simEventScheduler.oneshotToday(17,30,0, event1_on)
            simEventScheduler.oneshotRelativeToEvent(event1_on, 3600, event1_off)

            # post the "on" event for device2 to the event queue (lasts 3 hours)
            simEventScheduler.oneshotToday(19, 0, 0, event2_on)
            simEventScheduler.oneshotRelativeToEvent(event2_on, 10800, event2_off)

        else:

            # post the "on" event for device1 to the event queue
            # device has no start delay tolerance and expected on period is 2 hours
            simEventScheduler.oneshotToday(11, 0, 0, event1_on)
            simEventScheduler.oneshotRelativeToEvent(event1_on, 7200, event1_off)

            # post the "on" event for device1 to the event queue, on for 5 hours
            simEventScheduler.oneshotToday(18, 0, 0, event2_on)
            simEventScheduler.oneshotRelativeToEvent(event2_on, 18000, event2_off)



        # device3 scheduled "on" event, has estimated duration of 2 hours (120mins),
        # device has expected consumption of 20W, start delay tolerance of 4 hours (240mins) ,
        # and acitivity must be finished in 10 hours (600mins) from issued request
        event3 = DeviceOnRequestEvent(0, simContext.getDevice("sudjerica"), timedelta(minutes=120), 20)

        # post the "on" event for device3 to the event queue
        simEventScheduler.oneshotToday(20, 0, 0, event3)


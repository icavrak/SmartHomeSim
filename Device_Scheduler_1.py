from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from datetime import time
from datetime import timedelta

class Device_Scheduler_1(SpecialPurposeDevice):

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

        #scheduled "on" event for the non-managed device
        event1 = DeviceOnRequestEvent(0, simContext.getDevice("device1"))

        #post the "on" event to the event queue
        simEventScheduler.oneshotToday(time(9,0), event1)


        #device2 scheduled "on" event
        event2 = DeviceOnRequestEvent(0, simContext.getDevice("device2"))

        # device2 has no self-scheduled off, a request must be made to Controller by this scheduler
        # device2 is not a managed device, so absolute "off" time can be set for the off event
        event3 = DeviceOffRequestEvent(0, simContext.getDevice("device2"))

        #post those two events to simulation event queue
        simEventScheduler.oneshotToday(time(22,0), event2)
        simEventScheduler.oneshotRelativeToEvent(event2, timedelta(10800), event3)

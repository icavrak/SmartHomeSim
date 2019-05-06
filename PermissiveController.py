from ControllerDevice import ControllerDevice
from DeviceOnRequestEvent import DeviceOnRequestEvent
from DeviceOnEvent import DeviceOnEvent
from simulator import SmartHomeSim, EventScheduler

import simhelper

class PermissiveController(ControllerDevice):

    initialized = None

    def __init__(self):
        initialized = False

    def __init__(self, init):
        initialized = True

    def getDescription(self):
        return "Controller device >" + self.name + "< (single Controller device permitted in the system\nController device must be named '#controller'"

    def onRequest(self, event):

        #get Simulation Context and Event Scheduler objects
        simContext = self.getSimulationContext()

        #create new deviceON event with the same activation time as requested
        #in the requestOn event
        event = DeviceOnEvent(event.getCurrentTime(), event.getTargetDevice())
        simContext.addSimEvent(event)


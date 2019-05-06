from SpecialPurposeDevice import SpecialPurposeDevice
from DeviceOffEvent import DeviceOffEvent

class ControllerDevice(SpecialPurposeDevice):

    def onRequest(self, event):
        pass


    # default implementation of offRequest method:
    # all "off" requests are immediately granted and respective
    # DeviceOffEvent events are inserted into the simulation event queue
    def offRequest(self, event):

        # get Simulation Context and Event Scheduler objects
        simContext = self.getSimulationContext()

        # create new deviceOff event with the same deactivation time as requested
        # in the requestOff event
        event = DeviceOffEvent(event.getCurrentTime(), event.getTargetDevice())
        simContext.addSimEvent(event)


    def onNotice(self, event):
        pass


    def offNotice(self, event):
        pass


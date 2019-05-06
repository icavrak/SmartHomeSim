from SimulationEvent import SimulationEvent
from simulator import SmartHomeSim

class DeviceOffRequestEvent(SimulationEvent):

    def __init__(self, timestamp, targetDevice, requestingDevice=None):

        SimulationEvent.__init__(self, timestamp, self.dispatchRequest)

        self.targetDevice = targetDevice
        self.requestingDeviceName = requestingDevice


    def getCurrentTime(self):
        return self.getTimestamp()

    def getTargetDevice(self):
        return self.targetDevice

    def getRequestingDeviceName(self):
        return self.requestingDeviceName


    def dispatchRequest(self, self2):

        #get simulation context
        simContext = self.targetDevice.getSimulationContext()

        #get controller device
        controllerDevice = None
        controllerDevice = simContext.getDevice("#controller")

        #call onRequest scheduling method on controller device
        #with this event as the parameter
        if controllerDevice != None:
            controllerDevice.offRequest(self)




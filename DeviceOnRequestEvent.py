from SimulationEvent import SimulationEvent
from simulator import SmartHomeSim
from datetime import timedelta

class DeviceOnRequestEvent(SimulationEvent):

    #
    #Arguments:
    #
    #   timestamp               - unix timestamp, when the event is scheduled to happen (in simulated time)
    #   targetDevice            - reference to device the event is related to
    #   estimatedDuration       - hint on how many timedelta the device will run (may not be true, just a hint to the controller)
    #   estimatedConsumption    - estimated consumption in Watts (uniformly spread over the acivity period of the device)
    #   utilityInfo             - info object providing resulting utiliy of the device action (subclass of UtilityInfo class)
    #   requestingDevice        - reference to the requesting device for this event (scheduler or some other device)

    def __init__(self, timestamp, targetDevice, estimatedDuration=timedelta(minutes=0), estimatedConsumption=0, utilityInfo=None, requestingDevice=None):

        SimulationEvent.__init__(self, timestamp, self.dispatchRequest)

        #self.time = timestamp
        self.targetDevice = targetDevice
        self.requestingDeviceName = requestingDevice

        self.estimatedDuration = estimatedDuration
        self.estimatedConsumption = estimatedConsumption

        self.utilityInfo = utilityInfo


    def getCurrentTime(self):
        return self.getTimestamp()

    def getTargetDevice(self):
        return self.targetDevice

    def getRequestingDeviceName(self):
        return self.requestingDeviceName

    def getEstimatedDuration(self):
        return self.estimatedDuration

    def getEstimatedConsumption(self):
        return self.estimatedConsumption


    def getUtilityInfo(self):
        return self.utilityInfo

    def dispatchRequest(self, self2):

        #get simulation context
        simContext = self.targetDevice.getSimulationContext()

        #get controller device
        controllerDevice = None
        controllerDevice = simContext.getDevice("#controller")

        #call onRequest scheduling method on controller device
        #with this event as the parameter
        if controllerDevice != None:
            controllerDevice.onRequest(self)




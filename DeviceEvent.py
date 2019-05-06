from SimulationEvent import SimulationEvent


class DeviceEvent(SimulationEvent):

    def __init__(self, time=0, target=None):
        SimulationEvent.__init__(self, time, target)

    def getDeviceName(self):
        return self.getTarget().getName()

    def trigger(self):
        pass

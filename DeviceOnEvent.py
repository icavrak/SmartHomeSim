from DeviceEvent import DeviceEvent

class DeviceOnEvent(DeviceEvent):

    def __init__(self, time, targetDevice):
        DeviceEvent.__init__(self, time, targetDevice)

    def trigger(self):
        #self.target.on(self)
        self.getTarget().on()

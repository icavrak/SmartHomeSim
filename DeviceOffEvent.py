from DeviceEvent import DeviceEvent


class DeviceOffEvent(DeviceEvent):

    def __init__(self, time, targetDevice):
        DeviceEvent.__init__(self, time, targetDevice)

    def trigger(self):
        self.getTarget().off()

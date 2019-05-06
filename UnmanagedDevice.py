from Device import Device

class UnmanagedDevice(Device):

    def isManagedDevice(self):
        return False

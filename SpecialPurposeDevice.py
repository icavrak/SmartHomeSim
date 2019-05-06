from UnmanagedDevice import UnmanagedDevice

class SpecialPurposeDevice(UnmanagedDevice):

    def isManagedDevice(self):
        return False

    def getCurrentConsumption(self, time):
        return 0

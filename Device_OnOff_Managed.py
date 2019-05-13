from ManagedDevice import ManagedDevice
import simhelper

class Device_OnOff_Managed(ManagedDevice):

    def __init__(self):
        self.current_consumption = 0
        self.__on = False

    def __init__(self, init):
        self.current_consumption = float(init)
        self.__on = False

    def getDescription(self):
        return "Generic managed ON/OFF device >" + self.name + "< with constant consumption " + self.current_consumption + "W."

    def getCurrentConsumption(self, time):

        if self.__on == True:
            return self.current_consumption
        else:
            return 0

    def on(self):
        self.__on = True

    def off(self):
        self.__on = False

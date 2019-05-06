from abc import abstractmethod


class Device:

    __simulation = None  # type: SmartHomeSim
    __on = False         # type: bool
    __name = ""          # type: str

    ################################
    #
    #   Basic constructors
    #
    ################################

    def __init__(self, simulation):
        self.__on = False
        self.__name = None
        self.__simulation = None

    def __init__(self, name, init, simulation):
        self.__init__(self, simulation)


    ################################
    #
    #   Device description
    #
    ################################

    @abstractmethod
    def getDescription(self):
        pass

    @abstractmethod
    def isManagedDevice(self):
        pass

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def setSimulationContext(self, simulation):
        self.__simulation = simulation

    ################################
    #
    #   Device energy consumption
    #
    ################################

    #get device current consumption
    @abstractmethod
    def getCurrentConsumption(self, time):
        pass


    ####################################
    #
    #   Simulation init and cleanup
    #
    ####################################

    #device simulation init
    def deviceSimInit(self):
        pass

    #device simulation cleanup
    def deviceSimCleanup(self):
        pass


    ####################################
    #
    #   Simulation new date notification
    #   (should be ignored by devices)
    #
    ####################################

    #new date notification
    def onNewDate(self):
        pass

    ################################
    #
    #   Device on/off control
    #
    ################################

    #get device on/off status
    def isOn(self):
        return self.on

    #turn the device on
    @abstractmethod
    def on(self):
        pass

    #turn the device off
    @abstractmethod
    def off(self):
        pass

    ################################
    #
    #   Device mode control
    #
    ################################

    #does device support work modes
    def supportsModes(self):
        return False

    #get supported device modes
    def getSupportedModes(self):
        return None

    #set device's working mode
    def setMode(self):
        return False


    ################################
    #
    #   Device segmented operation
    #
    ################################

    #does device support opeating in segments
    def supportsSegments(self):
        if self.getSegments() == None:
            return False
        else:
            return True


     #return the list of segments
    def getSegments(self):
        return None


    ################################
    #
    #   Device communication
    #
    ################################

    #message reception callback function
    def receiveMessage(self, commMessage):
        return None


    ################################
    #
    #   Device accessor methods
    #   for context and device
    #   name
    #
    ################################

    def getSimulationContext(self):
        return self.__simulation

    def getDeviceName(self):
        return self.__name

    ################################
    #
    #   Methods for getting
    #   current user experience
    #   and experience predictions
    #
    ################################

    #default implementation - no experienceInfo
    #object attached to this device - no predictions
    #can be supplied to the controller
    def getUserExperienceInfo(self):
        return None

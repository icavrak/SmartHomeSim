from SimulationEvent import SimulationEvent


class SimTickEvent(SimulationEvent):

    __price = 0.0

    def __init__(self, time=0, target=None, price=0):

        SimulationEvent.__init__(self, time, target)
        self.__price = price


    #################################################
    #
    #       Event specific methods
    #
    #################################################

    def getCurrentPrice(self):
        return self.__price

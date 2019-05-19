from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from PriceInfo import PriceInfo
from datetime import timedelta
from datetime import time
from datetime import datetime
from FastOnUtilityInfo import FastOnUtilityInfo
from CummulativeUtilityInfo import CummulativeUtilityInfo


class Device_Scheduler_5(SpecialPurposeDevice):

    initialized = None

    def __init__(self):
        initialized = False

    def __init__(self, init):
        initialized = True

    def getDescription(self):
        return "Scheduler device >" + self.name + "<"


    def onNewDate(self):

        #get the simulation context object
        simContext = self.getSimulationContext()

        #get the scheduler helper object from the context
        simEventScheduler = simContext.getSimEventScheduler()



        ##########################
        #
        # TV scheduled "on" event
        #
        ##########################
        tv_duration = timedelta(hours=4)
        event2_on = DeviceOnRequestEvent(0, simContext.getDevice("tv"), tv_duration, 25.0)
        event2_off = DeviceOffRequestEvent(0, simContext.getDevice("tv"))

        # post the "on" event for device2 to the event queue (lasts 3 hours)
        simEventScheduler.oneshotToday(time(20, 0), event2_on)
        simEventScheduler.oneshotRelativeToEvent(event2_on, tv_duration, event2_off)


        ##########################
        #
        #   heater on event
        #
        ##########################
        #event4 = DeviceOnRequestEvent(0, simContext.getDevice("bojler"), timedelta(hours=3), 30.0)

        # post the "on" event for device4 to the event queue
        #simEventScheduler.oneshotToday(time(20, 0), event4)


    #############################################################
    #
    #   device initialization phase - setup the heater device
    #
    #############################################################

    def deviceSimInit(self):

        # get the simulation context object
        simContext = self.getSimulationContext()
        device = simContext.getDevice("bojler")

        # set utilities for devices (UtiliyInfo descendant classes implementing utiliy profiles
        # of devices (if not set, default utiliy for a device is AmbivalentUtilityInfo)
        tv_utility = FastOnUtilityInfo(simContext.getSimCurrentTime(), timedelta(seconds=1))
        simContext.getDevice("tv").setUtilityInfo(tv_utility)

        heater_utility = CummulativeUtilityInfo(simContext.getDevice("bojler"))
        simContext.getDevice("bojler").setUtilityInfo(heater_utility)

        #hot water heater capacity (liters)
        capacity = 80.0

        #hot water temperature consumption (liters)
        def lossF(current_temperature, dtime):
            assert (isinstance(current_temperature, float))
            assert( isinstance(dtime, datetime) )

            time = dtime.hour
            time2 = (dtime + timedelta(hours=1)).hour

            if dtime.isoweekday() < 5:
                valT = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 20.0, 20.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 30.0, 40.0, 20.0, 30.0, 50.0, 30.0, 20.0, 15.0)
            else:
                valT = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 20.0, 20.0, 30.0, 40.0, 40.0, 30.0, 10.0, 10.0, 10.0, 80.0, 80.0, 40.0, 30.0, 10.0, 10.0, 5.0)


            #fixed loss of 10% of difference bewtween water temperature and bathroom temperature per hour
            #fixed_loss = max(current_temperature - 20.0, 0.0) * 0.1

            #fixed loss of 0.26 degrees of celsius per hour
            fixed_loss = 0.50

            #variable loss of hot water consumption
            val1 = valT[time]
            val2 = valT[time2]
            val = val1 + (((val2 - val1) * dtime.minute) / 60)                           #current hot water consumption in liters
            new_temperature = val/capacity * 16.0 + (capacity-val)/capacity * current_temperature

            return fixed_loss + (current_temperature - new_temperature)


        #targeted hot water temperature
        def targetF(current_temperature, dtime):
            assert (isinstance(current_temperature, float))
            assert( isinstance(dtime, datetime) )
            time = dtime.hour
            #if dtime.isoweekday() < 5:
            #    valT = (
            #    30.0, 30.0, 30.0, 30.0, 30.0, 40.0, 50.0, 60.0, 60.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 50.0, 60.0, 60.0, 75.0,
            #    75.0, 75.0, 60.0, 40.0)
            #else:
            #    valT = (
            #    30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 50.0, 50.0, 50.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 75.0, 75.0,
            #    75.0, 75.0, 75.0, 75.0, 60.0, 40.0)

            #return valT[time]
            return 75.0


        def utilF(current_temperature, dtime, targetFunction):
            assert (isinstance(current_temperature, float))
            assert( isinstance(dtime, datetime) )
            assert( callable(targetFunction) )

            #calculate utility
            diffT = max(targetFunction(current_temperature, dtime) - current_temperature, 0) / 10
            if current_temperature >= 50.0:
                return 1.0
            else:
                return 1.0/(51.0-current_temperature)

        #set functions to device
        device.setLossFunction(lossF)
        device.setTargetFunction(targetF)
        device.setUtilityFunction(utilF)

        utilInfo = device.getUtilityInfo()
        assert( isinstance(utilInfo, CummulativeUtilityInfo) )
        utilInfo.setLossFunction(lossF)
        utilInfo.setTargetFunction(targetF)
        utilInfo.setUtilityFunction(utilF)
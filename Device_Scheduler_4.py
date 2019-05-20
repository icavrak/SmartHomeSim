from DeviceOffRequestEvent import DeviceOffRequestEvent
from DeviceOnRequestEvent import DeviceOnRequestEvent
from SpecialPurposeDevice import SpecialPurposeDevice
from PriceInfo import PriceInfo
from datetime import timedelta
from datetime import time
from datetime import datetime
from FastOnUtilityInfo import FastOnUtilityInfo
from CummulativeUtilityInfo import CummulativeUtilityInfo


class Device_Scheduler_4(SpecialPurposeDevice):

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

        #set utilities for devices (UtiliyInfo descendant classes implementing utiliy profiles
        #of devices (if not set, default utiliy for a device is AmbivalentUtilityInfo)
        tv_utility = FastOnUtilityInfo(simContext.getSimCurrentTime(), timedelta(seconds=1))
        simContext.getDevice("tv").setUtilityInfo(tv_utility)

        #heater_utility = RestrictedOffUtilityInfo(time(0, 0), time(9, 0))
        #simContext.getDevice("grijalica").setUtilityInfo(heater_utility)

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
        event4 = DeviceOnRequestEvent(0, simContext.getDevice("grijalica"), timedelta(hours=3), 30.0)

        # post the "on" event for device4 to the event queue
        simEventScheduler.oneshotToday(time(20, 0), event4)


    #############################################################
    #
    #   device initialization phase - setup the heater device
    #
    #############################################################

    def deviceSimInit(self):

        # get the simulation context object
        simContext = self.getSimulationContext()
        device = simContext.getDevice("grijalica")

        # set utility object for the heater device
        heater_utility = CummulativeUtilityInfo(device)
        device.setUtilityInfo(heater_utility)

        #model of outside temperature in 24 hours
        def lossF(current_temperature, dtime):
            assert (isinstance(current_temperature, float))
            assert( isinstance(dtime, datetime) )
            time = dtime.hour
            time2 = (dtime + timedelta(hours=1)).hour
            valT = (7.0,7.0,7.0,6.0,4.0,7.0,8.0,10.0,11.0,12.0,14.0,15.0,16.0,16.0,15.0,14.0,12.0,10.0,9.0,8.0,8.0,8.0,8.0,7.0)
            valM = (-12, - 10, -8, -4, 0, 6, 11, 10, 7, 0, -4, -8)
            val1 = valT[time]
            val2 = valT[time2]
            val = val1 + (((val2-val1) * dtime.minute) / 60)

            #changes of outside temperature offset during different months of year
            mOffset = dtime.month
            mOffset2 = (dtime + timedelta(days=31)).month
            valM1 = valM[mOffset]
            valM2 = valM[mOffset2]
            valMO = valM1 + (((valM2-valM1) * dtime.day) / 31)
            return current_temperature - (val + valMO)


        #room temperature target function
        def targetF(current_temperature, dtime):
            assert (isinstance(current_temperature, float))
            assert( isinstance(dtime, datetime) )

            time = dtime.hour

            #target temperature in degrees celsius (for weekdays and weekends separately)
            if( dtime.isoweekday() < 5 ):
                valT = (16, 16, 16, 16, 16, 16, 18, 22, 21, 16, 16, 16, 16, 16, 16, 21, 23, 23, 23, 23, 23, 23, 21, 18)
            else:
                valT = (16, 16, 16, 16, 16, 16, 18, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 19, 18)
            return valT[time]

        #utility function
        def utilF(current_temperature, dtime, targetFunction):
            assert (isinstance(current_temperature, float))
            assert( isinstance(dtime, datetime) )
            assert( callable(targetFunction) )

            #calculate difference between current and targeted temperature
            diffT = targetFunction(current_temperature, dtime) - current_temperature

            #if the temperature is higher than targeted for more than 2 degrees (overshoot),
            # lower utility to 0.8
            if diffT <= -2.0:
                return 0.8

            #if the temperature is up to 1 degree lower than targeted, utility is 1
            elif diffT <= 1.0:
                return 1.0
            #else the drop in utility is linear with the temperature difference
            else:
                return 1.0 - max(diffT/20.0, 1.0)

        #set functions to device
        device.setLossFunction(lossF)
        device.setTargetFunction(targetF)
        device.setUtilityFunction(utilF)

        # initialize utilityInfo with the same functions
        utilInfo = device.getUtilityInfo()
        assert( isinstance(utilInfo, CummulativeUtilityInfo) )
        utilInfo.setLossFunction(lossF)
        utilInfo.setTargetFunction(targetF)
        utilInfo.setUtilityFunction(utilF)
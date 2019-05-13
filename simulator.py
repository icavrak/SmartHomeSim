######################################################################
#
#					Imports
#
######################################################################
import json
import datetime
import argparse
import time
import Queue

from SimulationEvent import SimulationEvent
from SimTickEvent import SimTickEvent
from PriceInfo import PriceInfo

from simlogger import SimLogger
import simhelper

#######################################################################################################
#
#
#               C L A S S       E V E N T    S C H E D U L E R
#
#
#######################################################################################################

class EventScheduler():

    __simInstance = None

    #constructor
    def __init__(self, simContext):
        self.__simInstance = simContext

    def setSimContext(self, simContext):
        self.__simInstance = simContext

    #oneshot event at the current simulated day at specific time
    #returns true if the event has been inserted into the event queue
    #false if not
    def oneshotToday(self, moment, event):

        assert(isinstance(moment, datetime.time))
        assert (isinstance(event, SimulationEvent))

        #get current simulation date
        dateToday = self.__simInstance.getSimCurrentTime()

        #form YY-MM-DD HH:MM:SS timestamp
        newTime = datetime.datetime.combine(dateToday.date(), moment)

        #get UNIX timestamp for the specified datetime
        tstamp = simhelper.create_timestamp(newTime)

        #set event's timestamp
        event.setTimestamp(tstamp)

        #insert the event into the simulation event queue
        return self.__simInstance.addSimEvent(event, False)


    # oneshot event at the specified dateTime (argument is of datetime type)
    def oneshot(self, dateTime, event):

        assert (isinstance(dateTime, datetime.datetime))
        assert (isinstance(event, SimulationEvent))

        # get UNIX timestamp for the specified datetime
        tstamp = simhelper.create_timestamp(dateTime)

        #set event's timestamp
        event.setTimestamp(tstamp)

        #insert the event into the simulation event queue
        return self.__simInstance.addSimEvent(event, False)


    # oneshot event at the time offset (in sec) relative to the given timestamp (unix secs)
    def oneshotRelativeToTimestamp(self, baseTime, offset, event):

        assert(isinstance(baseTime, int))
        assert (isinstance(baseTime, int))
        assert (isinstance(event, SimulationEvent))

        #calculate timestamp for the newly scheduled event
        event.setTimestamp(baseTime + offset)

        # insert the event into the simulation event queue
        return self.__simInstance.addSimEvent(event, False)


    # oneshot event at the time offset (in sec) relative to the given event
    def oneshotRelativeToEvent(self, baseEvent, offset, event):

        assert (isinstance(baseEvent, SimulationEvent))
        assert (isinstance(offset, datetime.timedelta))
        assert (isinstance(event, SimulationEvent))

        return self.oneshotRelativeToTimestamp(baseEvent.getTimestamp(), offset.seconds, event)


    # oneshot event at the time offset (in sec) relative to the current simulation time
    def oneshotRelativeToNow(self, offset, event):

        assert (isinstance(offset, datetime.timedelta))
        assert (isinstance(event, SimulationEvent))

        return self.oneshotRelativeToTimestamp(simhelper.create_timestamp(self.__simInstance.getSimCurrentTime()), offset.seconds, event)


    #once every day at specific time, return: reference list to created and registered events
    def every_day(self, time, device, repeats=0):
        pass

    #once every working day at a specific time, return: reference list to created and registered events
    def every_workday(self, time, device, repeats=0):
        pass

    #once every weekend day at a specific time, return: reference list to created and registered events
    def every_weekend(self, time, device, repeats=0):
        pass






#######################################################################################################
#
#
#               C L A S S       S M A R T   H O M E   S I M
#
#
#######################################################################################################




######################################################################
#
#					Singleton decorator implementation
#
######################################################################
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class SmartHomeSim():

    ######################################################################
    #
    #					Singleton implementation
    #
    ######################################################################

    #__instance = None

    #@staticmethod
    #def getInstance():
    #   if SmartHomeSim.__instance == None:
    #        SmartHomeSim()
    #    return SmartHomeSim.__instance
    #
    #def __init__(self):
    #    if SmartHomeSim.__instance != None:
    #        raise Exception("ERROR: SmartHomeSim is a Singleton class")
    #    else:
    #        SmartHomeSim.__instance = self


    ######################################################################
    #
    #					Simulation settings
    #
    ######################################################################
    __setting_quiet = False
    __setting_gui_active = False

    __setting_sim_start_time = datetime.datetime.now()
    __setting_sim_end_time = None
    __setting_sim_time_step = 60

    __setting_devices_filename = None
    __setting_devices_data = None
    __setting_devices_registry = dict()

    __setting_pricing_profile = None
    __setting_pricing_profile_init = None
    __setting_price_horizon = 24


    ######################################################################
    #
    #					Simulation variables
    #
    ######################################################################
    __sim_eventqueue = Queue.PriorityQueue()

    __sim_started = time.time()
    __sim_current_time = __setting_sim_start_time
    __sim_current_date = ""

    __sim_total_consumption   = 0.0
    __sim_total_price         = 0.0

    __sim_pricing_profile = None

    __sim_price_total = 0
    __sim_consumption = 0.0

    __sim_simevent_scheduler = None
    __sim_price_helper = None

    ######################################################################
    #
    #					Simulation main log file
    #
    ######################################################################
    __log_filename = ''
    __log_handle = None

    # csv_name = ''

    ######################################################################
    #
    #					GUI Integration
    #
    ######################################################################
    __gui_signal_received = ""


    def post_sim_command(self, command):
        self.__gui_signal_received = command


    def set_consumption(self, consumption_received):
        # consumption per hour

        # IGOR: da li je ovo dobra formula?
        self.__sim_consumption = (consumption_received / 1000) / 60


    ######################################################################
    #
    #					Cached values
    #
    ######################################################################
    cached_current_date = None
    cached_profile = None


    ######################################################################
    #
    #					Device registry accessors
    #
    ######################################################################

    def getDevice(self, deviceName):

        deviceref = None
        try:
            deviceref = self.__setting_devices_registry[deviceName]
        except:
            pass
        return deviceref


    def getDeviceNames(self):
        return self.__setting_devices_registry.keys()


    ######################################################################
    #
    #					Simulation time accessors
    #
    ######################################################################

    def getSimStartTime(self):
        return self.__setting_sim_start_time

    def getSimCurrentTime(self):
        return self.__sim_current_time

    def getSimEndTime(self):
        return self.__setting_sim_end_time

    def isMonday(self):
        return self.__sim_current_time.isoweekday() == 1

    def isTuesday(self):
        return self.__sim_current_time.isoweekday() == 2

    def isWednesday(self):
        return self.__sim_current_time.isoweekday() == 3

    def isThursday(self):
        return self.__sim_current_time.isoweekday() == 4

    def isFriday(self):
        return self.__sim_current_time.isoweekday() == 5

    def isSaturday(self):
        return self.__sim_current_time.isoweekday() == 6

    def isSunday(self):
        return self.__sim_current_time.isoweekday() == 7

    def isWeekday(self):
        return self.isMonday() or self.isTuesday() or self.isWednesday() or self.isThursday() or self.isFriday()

    def isWeekend(self):
        return self.isSaturday() or self.isSunday()

    def getSimTimeStep(self):
        return self.__setting_sim_time_step

    ######################################################################
    #
    #			    Log file accessors
    #
    ######################################################################
    def getSimLogger(self):

        return self.__log_handle


    ######################################################################
    #
    #			    Simulation event queue accessors
    #
    ######################################################################

    def removeSimEvent(self, simulationEvent):
        simulationEvent.invalidate()


    def addSimEvent(self, simulationEvent, raise_exceptions = True):

        #check if simulation event is a descendant of SimulationEvent class
        if not isinstance(simulationEvent, SimulationEvent):
            if raise_exceptions:
                raise Exception("ERROR: event is not a SimulationEvent class descendant")
            else:
                return False

        #check if the event time is after the current simulation time
        if simulationEvent.getTimestamp() < simhelper.create_timestamp(self.__sim_current_time):
            if raise_exceptions:
                raise Exception("ERROR: simulation event timestamp preceeds the current simulated time")
            else:
                return False

        #check if the event time is before the end of simulation end
        if simulationEvent.getTimestamp() > simhelper.create_timestamp(self.__setting_sim_end_time):
            if raise_exceptions:
                raise Exception("ERROR: simulation event timestamp exceeds the simulated period")
            else:
                return False

        #add the event to the event queue
        self.__sim_eventqueue.put(simulationEvent)
        return True

    ######################################################################
    #
    #					Event Scheduler Helper object
    #
    ######################################################################

    def getSimEventScheduler(self):

        return self.__sim_simevent_scheduler


    ######################################################################
    #
    #					PriceInfo Helper object
    #
    ######################################################################

    def getPriceInfo(self):

        if self.__sim_price_helper == None:
            self.__sim_price_helper = PriceInfo(self, self.__sim_pricing_profile)
        return self.__sim_price_helper

    def getPriceHorizon(self):
        return self.__setting_price_horizon


    def getCurrentPrice(self):
        return self.__sim_pricing_profile.getCurrentPrice(self.__sim_current_time)


    ######################################################################
    #
    #			    Internal methods
    #
    ######################################################################


    def __loadClassInstance(self, module_name, class_name, init_parameters):

        module = __import__(module_name, fromlist=[class_name])
        loadedClass = getattr(module, class_name)

        if init_parameters:
            return loadedClass(init_parameters)
        else:
            return loadedClass()


    def __check_consistency(self):

        if self.__setting_sim_end_time == None:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: simulation end time not defined")
            return False

        if self.__setting_sim_start_time > self.__setting_sim_end_time:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: simulation end time precedes start time")
            return False

        if self.__setting_sim_time_step < 1:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: simulation time step too small or negative")
            return False

        if self.__setting_sim_time_step > 3600:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: simulation time step too large")
            return False

        if self.__setting_devices_data == None:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: simulation devices definition file not loaded")
            return False

        if self.__sim_pricing_profile == None:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: pricing profile class instance not created")
            return False

        if self.__setting_price_horizon < 1:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: pricing profile value not valid (" + str(self.__setting_price_horizon) + ")")
            return False

        if len(self.__setting_devices_registry) == 0:
            simhelper.reportNL(self.__setting_quiet, "\n   ERROR: device registry empty")
            return False


        return True



    def __loadDevices(self):

        deviceInitParms = None

        #for each device declared in the device list
        for deviceName in self.__setting_devices_data.keys():

            #reset init params for each device
            deviceInitParms = None
            try:
                #get the class name and init parameters (if any)
                deviceClassName = self.__setting_devices_data[deviceName]["class"]
                try:
                    deviceInitParms = self.__setting_devices_data[deviceName]["init"]
                except KeyError:
                    pass

                #get class instance and save it in the device registry
                deviceInstance = self.__loadClassInstance(deviceClassName, deviceClassName, deviceInitParms)
                self.__setting_devices_registry[deviceName] = deviceInstance

                #set device name and simulation context (this SmartHomeSim instance)
                deviceInstance.setName(deviceName)
                deviceInstance.setSimulationContext(self)

            except Exception as error:
                simhelper.reportNL(self.__setting_quiet, "\nError loading device >" + deviceName + "< definition: " + str(error))
                return False

        return True


    # consumption function is the target of SimTickEvent, and records current and total energy consumption
    # current consumption is calculated by polling all devices for their current consumption in the
    # observed simulation period determined by "sim-time-period" simulation parameter
    def __consumption(self, event):

        #variable for aggregating total consumption
        current_consumption = 0.0

        #for each device in the device registry
        for device in self.__setting_devices_registry:

            #get current consumption [Watts]
            current_consumption += self.__setting_devices_registry[device].getCurrentConsumption(self.__sim_current_time)

        #calculate total consumption for time period (according to simulation step) [Watt hours]
        total_consumption_delta = current_consumption * self.__setting_sim_time_step / 3600.0

        #calculate aggregate values
        self.__sim_total_consumption += total_consumption_delta
        self.__sim_total_price += total_consumption_delta * event.getCurrentPrice()

        #log data in log file or to console
        if self.__log_handle:
            self.__log_handle.logVariable("timestamp", event.getTimestamp())
            self.__log_handle.logVariable("consumption", current_consumption)
            self.__log_handle.logVariable("price", event.getCurrentPrice())
            self.__log_handle.logVariable("total_consumption", self.__sim_total_consumption)
            self.__log_handle.logVariable("total_price", self.__sim_total_price)
            self.__log_handle.writeToLog()
        else:
            simhelper.reportNL(self.__setting_quiet, str(event.getTimestamp()) + ", " + str(current_consumption) + ", " + str(event.getCurrentPrice())
                               + ", " + str(self.__sim_total_consumption) + ", " + str(self.__sim_total_price))


    # setup simulation data
    def __sim_setup(self):

        # load class definition containing simulation period and pricing schema
        # and instantiate an object of that class
        if self.__setting_pricing_profile:
            self.__sim_pricing_profile = self.__loadClassInstance(self.__setting_pricing_profile, self.__setting_pricing_profile, self.__setting_pricing_profile_init)
        else:
            return False

        # load device definition file (json)
        if self.__setting_devices_filename:
            with open(self.__setting_devices_filename) as devicefile:
                self.__setting_devices_data = json.load(devicefile)

        #populate device registry
        if self.__loadDevices() == False:
            return False

        # create logfile object (if path is defined) and register log variables
        if self.__log_filename:
            self.__log_handle = SimLogger()
            self.__log_handle.registerVariable("timestamp")
            self.__log_handle.registerVariable("consumption")
            self.__log_handle.registerVariable("price")
            self.__log_handle.registerVariable("total_consumption")
            self.__log_handle.registerVariable("total_price")

        #check if all mandatory settings are defined
        if not self.__check_consistency():
            return False

        #create SimEvent Scheduler helper object
        self.__sim_simevent_scheduler = EventScheduler(self)
        #self.__sim_simevent_scheduler.setSimContext(self)

        #generate time tick events and power prices for each moment in
        #the simulated period
        current_time = self.__setting_sim_start_time
        while current_time < self.__setting_sim_end_time:

            #get current price from profile
            current_price = self.__sim_pricing_profile.getCurrentPrice(current_time)

            #create SimTickEvent object and add it in the simulation event queue
            timestamp = simhelper.create_timestamp(current_time)
            self.__sim_eventqueue.put(SimTickEvent(timestamp, self.__consumption, current_price))

            # advance time for the specified simulation time step
            current_time += datetime.timedelta(seconds=self.__setting_sim_time_step)

        # call init for all devices (new log variables should be registered)
        for deviceName, deviceObject in self.__setting_devices_registry.iteritems():
            deviceObject.deviceSimInit()

        #logfile object - close the initialization phase and open the file
        if self.__log_handle:
            self.__log_handle.initialized()
            self.__log_handle.openLog(self.__log_filename)


        return True


    def __sim_loop(self):

        #while there are events in the simulation event queue...
        while not self.__sim_eventqueue.empty():

            #consume event from the main simulation event queue
            current_event = self.__sim_eventqueue.get()

            #if event has been invalidated, skip it
            if not current_event.isActive():
                continue

            #determine real time from simulation time
            self.__sim_current_time =  datetime.datetime.fromtimestamp(current_event.getTimestamp())

            #check if the simulation event is the first one for the given "real" date
            if self.__sim_current_time.date().isoformat() != self.__sim_current_date:

                #update current date
                self.__sim_current_date = self.__sim_current_time.date().isoformat()

                #notify all devices by calling the onNewDate() method
                for deviceName, deviceObject in self.__setting_devices_registry.iteritems():
                    deviceObject.onNewDate()

            #trigger action on event
            current_event.trigger()

            # check if pause gui signal exists
            if self.__gui_signal_received == "pause":
                # wait for another signal
                self.post_sim_command("")
                while self.__gui_signal_received == "":
                    time.sleep(0.5)
            elif self.__gui_signal_received == "stop":
                return True

        return True


    def __sim_cleanup(self):

        # call cleanup for all devices
        for deviceName, deviceObject in self.__setting_devices_registry.iteritems():
            deviceObject.deviceSimCleanup()

        # close logfile (if path is defined)
        if self.__log_handle != None:
            self.__log_handle.closeLog()

        return True


    ######################################################################
    #
    #			    Simulation run
    #
    ######################################################################

    # wait parametar
    # read only from json
    def run(self, waitForGUI = False):

        # setup simulation data
        simhelper.report(self.__setting_quiet, "Simulation setup....")
        status = self.__sim_setup()
        if status:
            simhelper.reportNL(self.__setting_quiet, "done")
        else:
            simhelper.reportNL(self.__setting_quiet, "... error during setup, simulation aborted.")
            return

        # if waitForGUI is set, wait for start signal from GUI
        if waitForGUI:
            while self.__gui_signal_received != "start":
                time.sleep(0.5)
                self.post_sim_command("")

        # main simulation loop
        simhelper.report(self.__setting_quiet, "Simulation start....")
        status = self.__sim_loop()
        if status:
            simhelper.reportNL(self.__setting_quiet, "done")
        else:
            simhelper.reportNL(self.__setting_quiet, "... error during simulation, simulation aborted.")

        # simulation cleanup
        simhelper.report(self.__setting_quiet, "Simulation cleanup....")
        status = self.__sim_cleanup()
        if status:
            simhelper.reportNL(self.__setting_quiet, "done")
        else:
            simhelper.reportNL(self.__setting_quiet, "... error during cleanup, simulation state not guaranteed.")



    ######################################################################
    #
    #			    Simulation initialization
    #
    ######################################################################

    def __parse_config_file(self, config_file):

        # load json file containing simulation configuration settings
        with open(config_file) as configfile:
            confdata = json.load(configfile)

        # set simulation devices json file name
        if confdata['devices-file']:
            self.__setting_devices_filename = confdata['devices-file']

        # set simulation start time from configuration file
        if confdata['sim-start-time']:
            self.__setting_sim_start_time = datetime.datetime.strptime(confdata["sim-start-time"], "%Y-%m-%d %H:%M:%S")

        # set simulation end time from configuration file
        if confdata['sim-end-time']:
            self.__setting_sim_end_time = datetime.datetime.strptime(confdata["sim-end-time"], "%Y-%m-%d %H:%M:%S")

        # set time step (in seconds) from configuration file
        if confdata['sim-time-step']:
            self.__setting_sim_time_step = int(confdata["sim-time-step"])

        # set pricing profile from configuration file
        if confdata['pricing-profile']:
            self.__setting_pricing_profile = confdata["pricing-profile"]

        # set pricing profile init data from configuration file
        if confdata['pricing-profile-init']:
            self.__setting_pricing_profile_init = confdata["pricing-profile-init"]

        # set pricing horizon data from configuration file
        if confdata['price-horizon']:
            self.__setting_price_horizon = int(confdata["price-horizon"])

        # set log filename from configuration file
        if confdata['logfile']:
            self.__log_filename = confdata["logfile"]

        # quiet operation mode from configuration file
        if confdata['quiet']:
            self.__setting_quiet = confdata["quiet"] == "True"



    def initialize(self, parser = None, config_filename = None):

        args = None

        if parser == None and config_filename == None:
            raise Exception("ERROR: SmartHomeSim no configuration source specified (neither command line arguments nor configuration file)")

        if parser != None:

            # initialize command line argument parser
            parser.add_argument("-d", "--devices-file", help="household setup file in json format")
            parser.add_argument("-c", "--config-file", help="simulation configuration file in json format")
            parser.add_argument("-s", "--sim-start-time", help="simulation start time, in YYYY-MM-DD hh:mm:ss format")
            parser.add_argument("-e", "--sim-end-time", help="simulation end time, in YYYY-MM-DD hh:mm:ss format")
            parser.add_argument("-t", "--sim-time-step", help="simulation time step, in seconds")
            parser.add_argument("-p", "--pricing-profile", help="simulation pricing profile, name of the python module (and class) implementing the pricing profile")
            parser.add_argument("-i", "--pricing-profile-init", help="initialization parameters for pricing profile")
            parser.add_argument("-l", "--logfile", help="output csv log file name")
            parser.add_argument("-ph", "--price-horizon", help="price horizon in hours (default 24 hours)")
            parser.add_argument("-q", "--quiet", action="store_true", help="enforce quiet operation (no console output")

            # parse command line arguments
            args = parser.parse_args()

            #get configuration file name
            if args.config_file:
                config_filename = args.config_file

        # parse configuration file (if specified)
        if config_filename:
            self.__parse_config_file(config_filename)

        if args != None:

            # set simulation devices json file name
            if args.devices_file:
                self.__setting_devices_filename = args.devices_file

            # set start time from command line argument (if specified)
            if args.sim_start_time:
                self.__setting_sim_start_time = datetime.datetime.strptime(args.sim_start_time, "%Y-%m-%d %H:%M:%S")

            # set end time from command line argument (if specified)
            if args.sim_end_time:
                self.__setting_sim_end_time = datetime.datetime.strptime(args.sim_end_time, "%Y-%m-%d %H:%M:%S")

            # set time step (in seconds) from command line argument (if specified)
            if args.sim_time_step:
                self.__setting_sim_time_step = int(args.sim_time_step)

            # set pricing profile module.class from command line argument (if specified)
            if args.pricing_profile:
                self.__setting_pricing_profile = args.pricing_profile

            # set pricing profile initialization parameters from command line argument (if specified)
            if args.pricing_profile_init:
                self.__setting_pricing_profile_init = args.pricing_profile_init

            # set price horizon from command line argument (if specified)
            if args.price_horizon:
                self.__setting_price_horizon = int(args.price_horizon)

            # set log filename from command line argument (if specified)
            if args.logfile:
                self.__log_filename = args.logfile

            # quiet operation mode from command line (if specified)
            if args.quiet:
                self.__setting_quiet = True


######################################################################
#
#			    Simulation start using command line
#
######################################################################
if __name__ == "__main__":

    simObject = SmartHomeSim()

    simObject2 = SmartHomeSim()

    simObject.initialize(parser = argparse.ArgumentParser())
    simObject.run()


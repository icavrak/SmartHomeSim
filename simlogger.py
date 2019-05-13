#################################################################
#
#					Imports
#
#################################################################
import csv

class SimLogger:

	__filewriter 	= None
	__log_columns 	= []

	__log_values	= None

	__ready 		= False
	__closed 		= False


	def __check_log_status(self):

		if self.__ready == False:
			raise Exception("SimLogger: Log initialization phase not concluded with a call to initialized()")

		if self.__closed == True:
			raise Exception("SimLogger: Log has been closed")


	#################################################################
	#
	#		Register log file column (initialization phase)
	#
	#################################################################

	def registerVariable(self, variable_name):

		if self.__ready == True:
			raise Exception("SimLogger: Log initialization phase already completed")

		self.__log_columns.append(variable_name)


	#################################################################
	#
	#				Conclude initialization phase
	#
	#################################################################
	def initialized(self):
		self.__ready = True

	def isInitialized(self):
		return self.__ready

	#################################################################
	#
	#				Open log file
	#
	#################################################################
	def openLog(self, logfileName):

		self.__check_log_status()

		loghandle = open(logfileName, 'w')
		self.__filewriter = csv.DictWriter(loghandle, fieldnames=self.__log_columns, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, restval='-')
		self.__filewriter.writeheader()


	def logVariable(self, variable_name, variable_value):

		self.__check_log_status()

		if not variable_name in self.__log_columns:
			raise Exception("SimLogger: Variable name not in the list of registered log variables")

		if self.__log_values == None:
			self.__log_values = dict()

		self.__log_values[variable_name] = variable_value


	#################################################################
	#
	#				Write log record
	#
	#################################################################
	def writeToLog(self):

		self.__check_log_status()
		#self.__filewriter.writerow([current_time, consumption, price, total_consumption, total_price])
		self.__filewriter.writerow(self.__log_values)

		self.__log_values = None



	#################################################################
	#
	#				Close log file
	#
	#################################################################
	def closeLog(self):

		self.__check_log_status()

		#self.__filewriter.close()
		self.__closed = True

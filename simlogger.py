#################################################################
#
#					Imports
#
#################################################################
import csv


#################################################################
#
#					Globals
#
#################################################################
filewriter = None


#################################################################
#
#				Open log file
#
#################################################################
def openLog(logfileName):
	
	global filewriter
	
	loghandle = open(logfileName, 'w')
	filewriter = csv.writer(loghandle, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['timestamp',  'current consumption', 'current price', 'total consumption', 'total price'])
	return loghandle
    
    
#################################################################
#
#				Write log record
#
#################################################################
def writeToLog(logHandle, current_time, consumption, price, total_consumption, total_price):

	filewriter.writerow([current_time, consumption, price, total_consumption, total_price])




#################################################################
#
#				Close log file
#
#################################################################
def closeLog(logHandle):

	logHandle.close()
	

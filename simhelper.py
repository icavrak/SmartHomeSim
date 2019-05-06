import time
import datetime
import sys


######################################################
#
#   Time format conversion functions
#
######################################################

def create_datetime(string_date):
    string_date = string_date.split("-")
    new_date = datetime.datetime(int(string_date[0]), int(string_date[1]), int(string_date[2]))
    return new_date

def create_timeofday(current_time):
    return current_time.strftime("%H:%M:%S")


def create_timestamp(dtime):
    return int(time.mktime(dtime.timetuple()))



######################################################
#
#   Report functions
#
######################################################

def report(quiet, string):
    if not quiet:
        sys.stdout.write(string)
        sys.stdout.flush()

def reportNL(quiet, string):
    if not quiet:
        print(string)
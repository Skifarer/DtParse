##Functions to add to datetime functionality

from os import times
import re
from datetime import datetime, date, time, timedelta
from math import floor

class DateTimeParse:
    #Change e.g. 07AUG89 to date
    def c7todate(date_str):
        if len(date_str) == 7 and re.match(r'\d{2}[A-Za-z]{3}\d{2}', date_str):
            return datetime.strptime(date_str,'%d%b%y').date()
        else:
            print('Invalid date string')
            return None
    
    #Change e.g. 103:12, 1735, 56:34, 31 to timedelta
    #Assume a single 2-digit number means minutes...
    def sToTD(timeStr):
        try:
            if timeStr.count(':') == 1:
                [hours, minutes, seconds] = timeStr.split(':') + ['0']
            elif timeStr.count(':') == 2:
                [hours, minutes, seconds] = timeStr.split(':')
            elif timeStr == '0':
                return timedelta(0)
            elif len(timeStr) == 2:
                return timedelta(minutes=int(timeStr))
            else:
                hours, minutes, seconds = timeStr[:-2], timeStr[-2:], '0'
            return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        except:
            print('Invalid timedelta string:', timeStr)
            raise

    def sToT(timeStr):
        try:
            if ':' in timeStr:
                [hours, minutes] = timeStr.split(':')
            else:
                hours, minutes = timeStr[:-2], timeStr[-2:]
            if int(hours) >= 24:
                print('Time after midnight, check!!', timeStr)
                hours = 23
                minutes = 59
            return time(hour=int(hours), minute=int(minutes))
        except:
            print('Invalid time string:', timeStr)
            raise
            

    #Change a timedelta to a string hh:mm
    def tdHMstr(td):
        hrs = floor(td.total_seconds()/3600)
        mins = int(round((td.total_seconds()/60)-(hrs*60),0))
        return '{:02d}:{:02d}'.format(hrs, mins)

    #Change e.g. 15:32 (time) to time
    def totd(time_str):
        if len(time_str) == 5 and re.match(r"\d{2}:[0-5]{1}\d{1}", time_str):
            return time(int(time_str[:2]),int(time_str[3:5]))
        else:
            print(time_str,'not a valid time string')
            return None

    #Change a date object to an AIMS date integer
    def toAimsDate(date_obj): 
        return (date_obj - date(1980, 1, 1)).days

    #Change an AIMS date integer into a date object
    def fromAimsDate(date_int):
        return date(1980,1,1) + timedelta(days = date_int)

    #Change a 4-digit string (e.g. 1545) to a time
    def t4toT(time_str):
        if time_str:
            return datetime.strptime(time_str, '%H%M').time()
        else:
            return datetime(2000,1,1).time()

    #Deal with times > 24:00 in a combine operation - takes datetime.date()
    #and string e.g. 24:00, 2556 etc
    def cleverCombine(dt, time_str, tzinfo):
        return datetime.combine(dt, time(), tzinfo=tzinfo) + DateTimeParse.sToTD(time_str)

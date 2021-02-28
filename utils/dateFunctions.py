import datetime
import time

# first day of week from given date
def fdow (datum):
    return datum  - datetime.timedelta(days=datum.weekday() % 7)


# last day of week from given date
def ldow (datum):
    return datum  - datetime.timedelta(days=datum.weekday() % 7) + datetime.timedelta(days=6)


# http://mvsourcecode.com/python-how-to-get-date-range-from-week-number-mvsourcecode/
def getDateRangeFromWeek(p_year,p_week):
    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek


# part represents how much letters from the day (0=all => 2=ma,di etc))
def daysInWeek(part=0):

    # all days in week in dutch, 
    days = ['maandag','dinsdag','woensdag','donderdag'
            ,'vrijdag','zaterdag','zondag']

    if part > 0:
        days = [day[:part].lower() for day in days]

    return days

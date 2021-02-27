import datetime
import time

# first day of week from given date
def fdow (datum):
    return datum  - datetime.timedelta(days=datum.weekday() % 7)


# last day of week from given date
def ldow (datum):
    return datum  - datetime.timedelta(days=datum.weekday() % 7) + datetime.timedelta(days=6)


def getDateRangeFromWeek(p_year,p_week):

    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek


# piece represents how much letters from the day (0=all => 2=ma,di etc))
def dagenInWeek(piece=0):

    # all days in week in dutch, 
    dagen = ['maandag','dinsdag','woensdag','donderdag'
            ,'vrijdag','zaterdag','zondag']

    if piece > 0:
        theReturn = [dag[:piece].lower() for dag in dagen]

    else:
        theReturn = dagen

    return theReturn
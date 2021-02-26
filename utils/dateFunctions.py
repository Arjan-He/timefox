import datetime


def fdow (datum):
    return datum  - datetime.timedelta(days=datum.weekday() % 7)


def dagenInWeek(piece=0):
    dagen = ['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag']

    if piece > 0:
        theReturn = [dag[:piece].lower() for dag in dagen]

    else:
        theReturn = dagen

    return theReturn
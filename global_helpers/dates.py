from datetime import timedelta, datetime as dt

def getDateXDaysAgo(daysAgo: int, date: str = None):
    if date is None:
        date= dt.today()
    else:
        date = dt.strptime(date, '%Y-%m-%d')

    theday, theDayString = getTimeDelta(date, daysAgo)

    dayOfWeek = checkWeekend(theDayString)
    
    if dayOfWeek == 'Sat':
        theday, theDayString = getTimeDelta(theday, 1)
        print ("Using next available date: " + theDayString)
    elif dayOfWeek == 'Sun':
        theday, theDayString = getTimeDelta(theday, 2)
        print ("Using next available date: " + theDayString)
    
    return theDayString

def checkWeekend(date: str):
    dateString = date
    date = dt.strptime(date, '%Y-%m-%d')
    weekNum = date.weekday()
    if weekNum == 5:
        print("Saturday Weekend date entered: " + dateString)
        return 'Sat'
    elif weekNum == 6:
        print("Sunday Weekend date entered: " + dateString)
        return 'Sun'
    elif weekNum == 4:
        print("Friday FriYAY")
        return 'Fri'
    else:
        return 'Weekday'

def getTimeDelta(date: dt, delta: int):
    newDate = date - timedelta(days=delta)
    newDateString = newDate.strftime('%Y-%m-%d')
    return newDate, newDateString

def check1mInterval(date):
    date = dt.strptime(date, '%Y-%m-%d')
    delta = (dt.today()-date).days
    if delta > 7:
        return False
    else:
        return True
import yfinance as yf
import global_helpers.dayHelper as dt

today = dt.getDateXDaysAgo(5)
if (today is not None):
    df = yf.download("META", start=today, period="1d", interval="1m")
    print (df)


parentDir = 'C:/Users/tynan/code_work_personal/savedTicks/'
#day is next folder
#ticker name is file name in folder

def getSavedDataOn(day):
    return

def getSavedTickerData(name):
    return
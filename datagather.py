from tradingview_screener import Query, Column as col
import yfinance as yf
from datetime import timedelta, datetime as dt
import os
import time

# print("Do you want to collect todays Data: Y/N")
# if input().lower() != 'y':
#     print("Y not inputted exiting script")
#     time.sleep(2)
#     exit()

n_rows, todaysData = (Query().set_markets('america')
       .select('name', 'close', 'volume', 'relative_volume_10d_calc', 'change')
       .where(
            col('Price').between(2, 25),
            col('relative_volume_10d_calc') > 1.2,
            col('Change %') > 5,
            #col('Exchange').like('nasdaq'),
            col('Volume') > 5000000
        )
        .order_by('volume', ascending=False)
        .limit(500)
        .get_scanner_data())

todaysTickers = [] 
for stock in todaysData.to_dict('records'):
    todaysTickers.append(stock['name'])

print(todaysData)

#theday = dt.today() - timedelta(days=6)
theday = dt.today()

today = theday.strftime('%Y-%m-%d')
parentDir = 'C:/Users/tynan/code_work_personal/savedTicks/'
pathString = parentDir+today

if os.path.exists(pathString):
    print("Error: day folder already exists")
    time.sleep(2)
    exit()

os.mkdir(pathString)

errorTicks = []
successTicks = []

for ticker in todaysTickers:
    try:
        df = yf.download(ticker, start=today, period="1d", interval="1m", progress=False)
        if len(df) == 0:
            print("Error trying to download ticker: " + ticker)
            errorTicks.append(ticker)
            continue
        df.to_csv(pathString+'/'+ticker)
        successTicks.append(ticker)
    except:
        print("Error trying to download ticker: " + ticker)
        errorTicks.append(ticker)

print("Here are todays success ticker downloads:")
print(successTicks)
print("Total Success Counnt: " + str(len(successTicks)))
if len(errorTicks) > 0:
    print("These tickers failed to download and save:")
    print(errorTicks)
    print("Total Error Count: " + str(len(errorTicks)))
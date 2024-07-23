import sys
sys.path.insert(0, 'global_helpers')

from tradingview_screener import Query, Column as col
import dataHelper as datahelp
import dates as dt
import os
import time


def gatherDataOnDay(today):
    if (today is None):
        print("No date provided return")
        return

    parentDir = 'C:/Users/tynan/code_work_personal/savedTicks/'
    pathString = parentDir+today

    if os.path.exists(pathString):
        print("Error: day " + today + " folder already exists")
        time.sleep(1)
        return

    os.mkdir(pathString)

    # print("Do you want to collect the days - " + today + " - Data: Y/N")
    # if input().lower() != 'y':
    #     print("Y not inputted exiting script")
    #     time.sleep(1)
    #     return()

    n_rows, todaysData = (Query().set_markets('america')
        .select('name', 'close', 'volume', 'relative_volume_10d_calc', 'change')
        .where(
                col('Price').between(2, 25),
                col('relative_volume_10d_calc') > 1.2,
                col('Change %') > 5,
                #col('Shares Float') > 2000000,
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

    
    errorTicks = []
    successTicks = []

    for ticker in todaysTickers:
        # try:
        df = datahelp.load_data(ticker, "1m", today)
        if len(df) == 0:
            print("Error trying to download ticker: " + ticker)
            errorTicks.append(ticker)
            continue
        df.to_csv(pathString+'/'+ticker)
        successTicks.append(ticker)
        # except:
        #     print("Big loop error trying to download ticker: " + ticker)
        #     errorTicks.append(ticker)

    print("Here are todays success ticker downloads:")
    print(successTicks)
    print("Total Success Counnt: " + str(len(successTicks)))
    if len(errorTicks) > 0:
        print("These tickers failed to download and save:")
        print(errorTicks)
        print("Total Error Count: " + str(len(errorTicks)))


for i in range(0,7):
    gatherDataOnDay(dt.getDateXDaysAgo(i))
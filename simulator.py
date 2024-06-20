import yfinance as yf
from datetime import datetime as dt
import pandas as pd
from datetime import timedelta
import numpy as np
import mplfinance as mpf
import io

""" But say you have one (or more) arguments in method1:
pip
def method1(param):
    return 'hello ' + str(param)

def method2(methodToRun):
    result = methodToRun()
    return result

Then you can simply invoke method2 as method2(lambda: method1('world')).

method2(lambda: method1('world'))
>>> hello world
method2(lambda: method1('reader'))
>>> hello reader """

def simulate_strategy_day(symbol, day, strategy):
    if dt.strptime(day, '%Y-%m-%d') < (dt.today() - timedelta(days=7)):
        print ("Error: the day you selected is more than 7 days ago")
        return 
    #first lets get the data for the day for the symbol
    df = yf.download(symbol, start=day, period="1d", interval="1m")
    
    #now we have the data we want to run our strategy on each 1m interval to see how we did
    #TODO
    #iterate on each row of data and call the strategy
    actionlist = []
    for row in df.itertuples():
        print("Data: " + row)
        action = strategy(row)
        actionlist.append(action)
        print("Result: "+ action)
    
    #make sure our x axis index is formatted property
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_localize(None)
    #data variable and formatting to display data on top off graph
    #now lets create our buy/sell/other important flags from our strategy data set to add as an overlay on the plot
    """ data = '''
    Time Price
    "2022-06-07 11:20:00" 412.66
    "2022-06-07 12:30:00" 411.350
    "2022-06-07 13:50:00" 413.290
    "2022-06-07 15:00:00" 414.109
    "2022-06-09 13:25:00" 409.660
    "2022-06-10 09:50:00" 394.130
    '''
    sell_df = pd.read_csv(io.StringIO(data), delim_whitespace=True)
    sell_df['Time'] = pd.to_datetime(sell_df['Time'])
    sell_df.set_index('Time', inplace=True)
    sell_df = sell_df.reindex(df.index, axis='index', fill_value=np.NaN)
    apdict = mpf.make_addplot(sell_df['Price'], type='scatter', markersize=200, marker='^') """
    
    #candlestick ploit the data for the day
    mpf.plot(df,
         type="candle", 
         title = "Stock: "+symbol+" Day: "+day,  
         style="yahoo", 
         volume=True, 
         figratio=(20.00, 6.75),
         returnfig=True,
         show_nontrading=False
         #addplot=apdict
    )
    mpf.show()
    
    return

simulate_strategy_day("META", dt.today().strftime('%Y-%m-%d'), "s")
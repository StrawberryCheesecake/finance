import yfinance as yf
import pandas as pd
from src.global_helpers import dayHelper as dt
import os
#import grapher

def buyOrSellVol(data):
    if data['close'] > dota['open']:
        return 'buy'
    else:
        return 'sell'

def check_symbol_is_real(symbol: str) -> bool:
      ticker = yf.Ticker(symbol)
      info = None
      try:
            info = ticker.info
            return True
      except:
            return False

def check_tp_exists(symbol: str, date: str) -> bool:
      """Check if a ticker profile of the same symbol and date exists"""
      base_directory = './backend/data/'
      file_path = os.path.join(base_directory, symbol, f"{date}.pkl")
      if os.path.exists(file_path):
            return True
      return False

def load_data(symbol: str, interval: str, start_date: str, end_date: str = None):
      """Gets the data for the passed symbol with a given interval, start date and end date
      \n If no end date is passed it will assume that you want the data just for the start date passed"""
      if end_date is not None:
            print("Loading Data for ticker: " + symbol + " with interval: " + interval + " and date range start: " + start_date + " end: " + end_date)
            if not dt.check1mInterval(end_date):
                  raise Exception('Error end date out of range for 1m interval:' + end_date)
      else:
            print("Loading Data for ticker: " + symbol + " with interval: " + interval + " and date: " + start_date)
            dayOfWeek = dt.checkWeekend(start_date)
            if dayOfWeek == 'Fri':
                  end_date = dt.getDateXDaysFrom(-3,start_date)
            else:
                  end_date = dt.getDateXDaysFrom(-1,start_date)
      if interval == '1m':
            #make sure start date and end date are within 30 days
            if not dt.check1mInterval(start_date):
                  raise Exception('Error start date out of range for 1m interval: ' + start_date)
      if start_date == end_date:
            raise Exception("Error start/end dates cannot be the same: " + start_date + " " + end_date)
      
      data = yf.download(symbol, start=start_date, end=end_date, interval=interval, progress=False)
      tempIndex = pd.to_datetime(data.index).date
      dfs = [g for _,g in data.groupby(tempIndex)]

      if len(dfs) < 2:
            return dfs[0]
      else: 
            return dfs

#test = load_data('MIRA', '1m', '2024-07-22')
#print(test.columns)
#print(test['Open'][0])
#print(test.index[0])
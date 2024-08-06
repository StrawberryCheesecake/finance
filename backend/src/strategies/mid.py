import yfinance as yf
from datetime import datetime as dt
import pandas as pd
from datetime import timedelta
import numpy as np
import mplfinance as mpf
#import io

from src.portfolios import tickerPortfolio as tp

from src.global_helpers import dayHelper as dates

#every strategy function shall return a dictionary result which contains the action to perform, and the quantity
#action = buy, sell, hold
#quantity = how many shares
#type = limit? trail? unsure

#the strategy for basic we will implement will be to look at the current instance of data and if it lower than the previous days high by 20% buy and if it is higher than the previous days high by 20% sell, inbetween will be hold
#this strategy clearly has a lot of holes in it such as if the stock is downwards trending it will continuously buy but we will ignore that for this basic case as it is a POC
def basic_3xdropbuy_10percdropsell(tickerPortfolio: tp):
    result = {
        'name': "3xdrop10psell",
        'action': None,
         #'type': None,
        # 'price': None,
        'quantity': None #IN SHARES YOU DUMB DUMB
    }
    daily_data = tickerPortfolio.daily_data_cache
    #for price in reversed(daily_data):
        #check if we are in a invested or open position
        #if open
            #check if the price is green after the last 3-5 sequences are red if so buy 10% of vol
            #if more than 5 dont buy hold
            #if less than 3 hold
        #if invested
            #check if current price is < 10% previous data close if so sell
            #else hold
    result['action'] = 'buy'
    result['quantity'] = 1
    return result

#ticker_portfolio = tp('AAPL', dates.getDateXDaysAgo(0), 500.00)
#ticker_portfolio.add_strategy(basic_3xdropbuy_10percdropsell, 'mid')
#result =ticker_portfolio.live_execute_strategies()
import os, sys
sys.path.insert(0, 'global_helpers')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tickerPortoflio import tickerPortfolio as tp
import dataHelper as dh

def simulateTickerHistoric(tickerPortfolio: tp):
    theday = tickerPortfolio.date
    symbol = tickerPortfolio.symbol
    #current_balance = tickerPortfolio.principal
    days_data = dh.load_data(symbol, '1m', theday)
    for item in days_data:
        tickerPortfolio.load_live_data(item)
        tickerPortfolio.live_execute_strategies()
    tickerPortfolio.save_to_file()
    return

def simulateTickerFromSave(symbol: str, date: str):
    tickerPortfolio = tp.load_from_file(symbol, date)
    days_data = tickerPortfolio.daily_data_cache
    tickerPortfolio.clear_portfolio_data()
    for item in days_data:
        tickerPortfolio.load_live_data(item)
        tickerPortfolio.live_execute_strategies()        
    tickerPortfolio.save_to_file()
    return
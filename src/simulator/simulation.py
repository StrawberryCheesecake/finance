import sys
sys.path.insert(0, 'src')

from portfolios import tickerPortfolio as tp
from global_helpers import dataHelper as dh

def simulateTickerHistoric(tickerPortfolio: tp, save: bool = False) -> tp.tickerPortfolio:
    """Pass and simulate a ticker portfolio, will return the ticker portfolio"""
    theday = tickerPortfolio.date
    symbol = tickerPortfolio.symbol
    #current_balance = tickerPortfolio.principal
    #execute pre market strats
    # print("Executing pre-market strategies")
    #tickerPortfolio.pre_execute_strategies()
    days_data = dh.load_data(symbol, '1m', theday)
    print("Executing mid-market simulation")
    for row in days_data.iterrows():
        tickerPortfolio.load_live_data(row)
        #execute during market strats
        tickerPortfolio.mid_execute_strategies()
    print("Completed mid-market simulation")
    #execute post market strats
    # print("Executing post-market strategies")
    #tickerPortfolio.post_execute_strategies()
    print("Simulation complete saving file")
    if save:
        tickerPortfolio.save_to_file()
    return tickerPortfolio

def simulateTickerFromSave(symbol: str, date: str, save:bool = False) -> tp.tickerPortfolio:
    """Simulate a ticker portfolio from a save file directly, will return the ticker portfolio"""
    tickerPortfolio = tp.tickerPortfolio.load_from_file(symbol, date)
    days_data = tickerPortfolio.daily_data_cache
    tickerPortfolio.clear_portfolio_data()

    # print("Executing pre-market strategies")
    #tickerPortfolio.pre_execute_strategies()
    print("Executing mid-market simulation")
    for item in days_data:
        tickerPortfolio.load_live_data(item)
        tickerPortfolio.mid_execute_strategies()        
    print("Completed mid-market simulation")
    # print("Executing post-market strategies")
    #tickerPortfolio.post_execute_strategies()
    print("Simulation complete saving file")
    if save:
        tickerPortfolio.save_to_file()
    return tickerPortfolio
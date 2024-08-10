import yfinance as yf
from src.portfolios import tickerPortfolio as tp
from src.strategies import mid, optimal
from src.simulator import simulation as sim

portfolio = tp.tickerPortfolio(symbol="EGY", date="today", principal=10000.0)
# portfolio.add_strategy(mid.basic_3xdropbuy_10percdropsell, 'mid')
portfolio.load_daily_data()
result = portfolio.to_json()
# sim.simulateTickerHistoric(portfolio)
print(result)

# portfolio = tp.tickerPortfolio.load_from_file("AAPL", "2024-07-24")
# # sim.simulateTickerHistoric(portfolio)
# optimal.findOptimalEntryExit(portfolio)
# # print(portfolio)

# portfolio = tp.tickerPortfolio(symbol="META", date="today", principal=10000.0)
# portfolio.load_daily_data()
# portfolio.save_to_file()
# portfolio = tp.tickerPortfolio.load_from_file("META", "2024-08-01")
# portfolio.add_strategy(mid.basic_3xdropbuy_10percdropsell, 'mid')
# # portfolio.add_strategy(mid.basic_3xdropbuy_10percdropsell, 'mid')
# print(portfolio)
# sim.simulateTickerHistoric(portfolio)
# # print(portfolio)

# portfolio = sim.simulateTickerFromSave("META", "2024-08-01")
# print(portfolio)





# import global_helpers.dayHelper as dt
#import grapher
# import global_helpers.dataHelper as dh
#stock screener website https://finviz.com/
#maybe use this to start filtering and downloading ticker data?

# def simulate_strategy_day(symbol, day, strategy):
    
#     #first lets get the data for the day for the symbol
#     df = yf.download(symbol, start=day, period="1d", interval="1m")

#     #test dumb data
#     symbol2 = "AAPL"
#     df2 = yf.download(symbol2, start=day, period="1d", interval="1m")
#     triggers = {}
    
#     #now we have the data we want to run our strategy on each 1m interval to see how we did
#     #TODO
#     #iterate on each row of data and call the strategy
#     #strategy should return respective action for that period
#     # actionlist = []
#     # for row in df.itertuples():
#     #     print("Data: " + row)
#     #     action = strategy(row)
#     #     actionlist.append(action)
#     #     print("Result: "+ action)
    
#     #once we have all our actions we cumulate them into a triggers dataframe to add to graph data and pass

#     graphData = {symbol: [df,day,triggers], symbol2: [df2,day]}
#     save = False
#     grapher.candleStickMaker(graphData, save)

#     return




# #today = dt.getDateXDaysAgo(5)
# #if (today is not None):
# #    simulate_strategy_day("META", today, "s")

# test = dh.load_data('META',dt.getDateXDaysAgo(5),'1m','5d')
# print(test)
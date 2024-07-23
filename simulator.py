import yfinance as yf
import global_helpers.dates as dt
#import grapher
import global_helpers.dataHelper as dh
#stock screener website https://finviz.com/
#maybe use this to start filtering and downloading ticker data?

def simulate_strategy_day(symbol, day, strategy):
    
    #first lets get the data for the day for the symbol
    df = yf.download(symbol, start=day, period="1d", interval="1m")

    #test dumb data
    symbol2 = "AAPL"
    df2 = yf.download(symbol2, start=day, period="1d", interval="1m")
    triggers = {}
    
    #now we have the data we want to run our strategy on each 1m interval to see how we did
    #TODO
    #iterate on each row of data and call the strategy
    #strategy should return respective action for that period
    # actionlist = []
    # for row in df.itertuples():
    #     print("Data: " + row)
    #     action = strategy(row)
    #     actionlist.append(action)
    #     print("Result: "+ action)
    
    #once we have all our actions we cumulate them into a triggers dataframe to add to graph data and pass

    graphData = {symbol: [df,day,triggers], symbol2: [df2,day]}
    save = False
    grapher.candleStickMaker(graphData, save)

    return




#today = dt.getDateXDaysAgo(5)
#if (today is not None):
#    simulate_strategy_day("META", today, "s")

test = dh.load_data('META',dt.getDateXDaysAgo(5),'1m','5d')
print(test)
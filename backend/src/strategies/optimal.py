from src.portfolios import tickerPortfolio as tp
import numpy as np
#from scipy.signal import argrelextrema as argl

# x = np.array([np.float64(224.0), np.float64(224.375), np.float64(224.60000610351562), np.float64(224.35000610351562), np.float64(223.89999389648438), np.float64(222.8800048828125), np.float64(222.8000030517578), np.float64(222.00999450683594), np.float64(221.99049377441406), np.float64(221.63409423828125), np.float64(221.41160583496094)])
# y = argl(x, np.greater)
# print(y)


def findOptimalEntryExit(tickerP: tp):
    time = []
    open =  np.zeros(shape=(len(tickerP.daily_data_cache), 1))
    close = np.zeros(shape=(len(tickerP.daily_data_cache), 1))
    for index,item in enumerate(tickerP.daily_data_cache):
        time.append(item[0])
        open[index] = item[1]['Open']
        close[index] = item[1]['Close']
    # print(open)
    # print(time)
    #returns first array of max and second array to ignore
    mins = argl(open, np.less)[0]
    maxs = argl(open, np.greater)[0]
    print(mins)
    print(maxs)

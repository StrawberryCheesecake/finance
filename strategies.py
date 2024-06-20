
import yfinance as yf
from datetime import datetime as dt
import pandas as pd
from datetime import timedelta
import numpy as np
import mplfinance as mpf
import io

#every strategy function shall return as a baseline, the result object which will contain the information required
class result:
        #at a baseline the result will always return back an action to perform
        action = None

#the strategy for basic we will implement will be to look at the current instance of data and if it lower than the previous days high by 20% buy and if it is higher than the previous days high by 20% sell, inbetween will be hold
#this strategy clearly has a lot of holes in it such as if the stock is downwards trending it will continuously buy but we will ignore that for this basic case as it is a POC
def basic(data, day, inst, status):
    r = result()
    print (r.action)
    r.action = "hold"
    
    return r

print(basic(1,2,3).action)
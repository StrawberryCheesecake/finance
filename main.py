#api key 6OTO8B7B86VTLIY4 alpha vantage
import yfinance as yf
import simulator as sim
from datetime import datetime as dt

sim.simulate_strategy_day("META", dt.today().strftime('%Y-%m-%d'), "s")


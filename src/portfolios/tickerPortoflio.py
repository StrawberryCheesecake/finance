import sys
sys.path.insert(0, 'global_helpers')

import pandas as pd
from typing import Callable, List
import dates as dates
import dataHelper as dataHelp
from typing import Literal 
import pickle
import os

class tickerPortfolio:
    base_directory = 'C:/Users/tynan/code_work_personal/savedPortfolios/'
    def __init__(self, symbol: str = None, date: str = None, principal: float = None):      
        self.symbol = symbol
        self.date = date
        self.principal = principal

        self.current_balance = principal
        self.net_gain_loss = 0
        self.final_balance = 0
        self.strategy_investment_tracker = {}
        self.daily_data_cache = []
        self.action_cache = []
        
        self.pre_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        self.mid_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        self.post_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        
        if symbol is not None and date is not None:
            #get the last year of general data
            self.historic_data = dataHelp.load_data(symbol, '1d', dates.getDateXDaysAgo(365,date), date)

            #Get the last 3 days of detailed data
            self.previous_days_data = dataHelp.load_data(symbol, '1m', dates.getDateXDaysAgo(3,date), date)
        else:
            self.historic_data = None
            self.previous_days_data = None

    def clear_portfolio_data(self):
        self.current_balance = self.principal
        self.net_gain_loss = 0
        self.final_balance = 0
        self.strategy_investment_tracker = {}
        self.daily_data_cache = []
        self.action_cache = []

        return
    
    def clear_portfolio_strategies(self):
        self.pre_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        self.mid_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        self.post_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        return

    #TODO add ability to account for type of sale/purchase AKA limit sale/buy
    #add a type and price key to the tracker dictionary see if the price is > open? buy is possible if price is < open sell if possible
    #this seems lower in the prio since limit can be tracked in strategy? 
    def load_live_data(self, data):
        self.daily_data_cache.append(self.current_data)
        cur_price = data['Open']
        time = data.index
        #iterate through strat invest tracker
        #implement actions(update balances) and perform checks
        for name, strat in self.strategy_investment_tracker:
            act = strat['action']
            quant = strat['quantity']
            totes = strat['total']
            t_amount = quant*cur_price
            if act == 'buy':
                #we assume any purchase and sale is possible because the total volume should be kept less than 20% of prinicpal
                self.current_balance -= t_amount
                self.action_cache.append({'action': 'buy', 'amount': quant, 'time': time})
            elif act == 'sell':
                self.current_balance += t_amount
                self.action_cache.append({'action': 'sell', 'amount': quant, 'time': time})
            #action executed reset tracker
            self.strategy_investment_tracker[name] = {'action': None, 'quantity': 0, 'total': totes}
        
    def live_execute_strategies(self):
        #iterate through all strategies accumulate list of results
        action_list = []
        if self.current_data is None:
            print("Executing pre-market strategies")
            for strategy in self.pre_market_strategies:
                action_list.append(strategy(self))
        elif self.current_data == "end":
            print("Executing post-market strategies")
            for strategy in self.post_market_strategies:
                action_list.append(strategy(self))
        else:
            print("Executing mid-market strategies")
            for strategy in self.mid_market_strategies:
                action_list.append(strategy(self))
        
        #process results 
        for result in action_list:
            sname = result['name']
            action = result['action']
            quantity = result['quantity']

            entry = self.strategy_investment_tracker.get(sname, {'action': None, 'quantity': 0, 'total': 0})

            if action == 'buy':
                entry['action'] = 'buy'
                entry['total'] += quantity
            elif action == 'sell':
                entry['action'] = 'sell'
                entry['total'] -= quantity
            elif action == 'hold':
                entry['action'] = 'hold'
            entry['quantity'] = quantity

            self.strategy_investment_tracker[sname] = entry

    def add_strategy(self, strategy: Callable[['tickerPortfolio'], dict], market_phase: Literal['pre', 'mid', 'post']):
        if market_phase == 'pre':
            self.pre_market_strategies.append(strategy)
        elif market_phase == 'mid':
            self.mid_market_strategies.append(strategy)
        elif market_phase == 'post':
            self.post_market_strategies.append(strategy)
        else:
            raise ValueError("Invalid market phase. Choose from 'pre_market', 'mid_market', 'post_market'.")

    def save_to_file(self):
        print("Saving Portfolio: "+self.symbol+" " + self.date)
        if not self.symbol or not self.date:
            raise ValueError("Symbol and date must be set to save the strategy.")
        
        folder_path = os.path.join(tickerPortfolio.base_directory, self.symbol)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{self.date}.pkl")
        
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(symbol: str, date: str):
        print("Loading Portfolio: "+symbol+" " + date)
        file_path = os.path.join(tickerPortfolio.base_directory, symbol, f"{date}.pkl")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No strategy file found for {symbol} on {date}.")
        
        with open(file_path, 'rb') as file:
            return pickle.load(file)


# ticker_strategy = tickerStrategy('AAPL', dates.getDateXDaysAgo(0), 500.00)
# ticker_strategy.save_to_file()
# loaded_tick = tickerStrategy.load_from_file('asd', dates.getDateXDaysAgo(0))
# print(loaded_tick.historic_data)

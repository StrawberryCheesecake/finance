import pandas as pd
import os
from typing import Callable, List
from src.global_helpers import dayHelper as dates
from src.global_helpers import dataHelper as dataHelp
from typing import Literal 
import pickle
import json

class tickerPortfolio:
    base_directory = './backend/data/'
    def __init__(self, symbol: str = None, date: str = None, principal: float = None):
        if date == "today":
            date = dates.getDateXDaysFrom(0)      
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
            print("Loading historical data for ticker portfolio")
            #get the last year of general data
            self.historic_data = dataHelp.load_data(symbol, '1d', dates.getDateXDaysFrom(365,date), date)

            #Get the last 3 days of detailed data
            self.previous_days_data = dataHelp.load_data(symbol, '1m', dates.getDateXDaysFrom(3,date), date)
            print("Completed downloading historical data for ticker portfolio")
        else:
            self.historic_data = None
            self.previous_days_data = None

    def to_dict(self) -> dict:
        """Converts the portfolio to a JSON-serializable dictionary."""
        temp_daily_data = []
        for item in self.daily_data_cache:
            temp_daily_data.append({
                'x': dates.dateToString(item[0]),
                'y': [
                    int(item[1]['Open']*100)/100,
                    int(item[1]['High']*100)/100,
                    int(item[1]['Low']*100)/100,
                    int(item[1]['Close']*100)/100,
                    item[1]['Volume']]
                })
        
        return {
            "symbol": self.symbol,
            "date": self.date,
            "principal": self.principal,
            "current_balance": self.current_balance,
            "net_gain_loss": self.net_gain_loss,
            "final_balance": self.final_balance,
            "strategy_investment_tracker": self.strategy_investment_tracker,
            "daily_data_cache": temp_daily_data,
            "action_cache": self.action_cache,
            "pre_market_strategies": [func.__name__ for func in self.pre_market_strategies],
            "mid_market_strategies": [func.__name__ for func in self.mid_market_strategies],
            "post_market_strategies": [func.__name__ for func in self.post_market_strategies],
            #"historic_data": self.historic_data if self.historic_data is not None else None,
            #"previous_days_data": self.previous_days_data if self.previous_days_data is not None else None,
        }

    @staticmethod
    def from_dict(data: dict) -> 'tickerPortfolio':
        """Creates a tickerPortfolio instance from a dictionary."""
        portfolio = tickerPortfolio(
            symbol=data["symbol"],
            date=data["date"],
            principal=data["principal"],
        )
        portfolio.current_balance = data["current_balance"]
        portfolio.net_gain_loss = data["net_gain_loss"]
        portfolio.final_balance = data["final_balance"]
        portfolio.strategy_investment_tracker = data["strategy_investment_tracker"]
        portfolio.daily_data_cache = [pd.DataFrame(cache) for cache in data["daily_data_cache"]]
        portfolio.action_cache = data["action_cache"]
        # Note: For strategies, you need to map back to the actual functions
        portfolio.pre_market_strategies = []  # Fill with actual function references if needed
        portfolio.mid_market_strategies = []  # Fill with actual function references if needed
        portfolio.post_market_strategies = []  # Fill with actual function references if needed
        portfolio.historic_data = pd.DataFrame(data["historic_data"]) if data["historic_data"] is not None else None
        portfolio.previous_days_data = pd.DataFrame(data["previous_days_data"]) if data["previous_days_data"] is not None else None
        return portfolio

    def to_json(self) -> str:
        """Converts the portfolio to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)

    @staticmethod
    def from_json(json_str: str) -> 'tickerPortfolio':
        """Creates a tickerPortfolio instance from a JSON string."""
        return tickerPortfolio.from_dict(json.loads(json_str))

    def __str__(self):
        return (
            f"TickerPortfolio(\n"
            f"  symbol={self.symbol},\n"
            f"  date={self.date},\n"
            f"  principal={self.principal},\n"
            f"  current_balance={self.current_balance},\n"
            f"  net_gain_loss={self.net_gain_loss},\n"
            f"  final_balance={self.final_balance},\n"
            f"  strategy_investment_tracker={self._dict_summary(self.strategy_investment_tracker)},\n"
            f"  daily_data_cache={self._list_summary(self.daily_data_cache)},\n"
            f"  action_cache={self._list_summary(self.action_cache)},\n"
            f"  pre_market_strategies={self._strategy_summary(self.pre_market_strategies)},\n"
            f"  mid_market_strategies={self._strategy_summary(self.mid_market_strategies)},\n"
            f"  post_market_strategies={self._strategy_summary(self.post_market_strategies)},\n"
            f"  historic_data_available={'Yes' if self.historic_data else 'No'},\n"
            f"  previous_days_data_available={'No' if self.previous_days_data.empty else 'Yes'}\n"
            f")"
        )

    def _list_summary(self, lst: List[any]) -> str:
        """Provides a summary of a list including its length and contents."""
        sample = lst[0] if lst else 'None'
        return f"len={len(lst)}, contents={sample}"

    def _dict_summary(self, d: dict) -> str:
        """Provides a summary of a dictionary including its length and all key-value pairs."""
        if d:
            first_key = next(iter(d))
            sample = {first_key: d[first_key]}
        else:
            sample = 'None'
        return f"len={len(d)}, sample={sample}"

    def _strategy_summary(self, strategies: List[Callable]) -> str:
        """Provides a summary of strategy functions including their count and names."""
        strategy_names = [strategy.__name__ for strategy in strategies]
        return f"count={len(strategies)}, strategy_names={strategy_names}"

    def clear_portfolio_data(self) -> None:
        """
        Resets the portfolio's financial data and caches to their initial states.
        
        Sets current balance to the initial principal, resets net gain/loss,
        clears the strategy investment tracker, daily data cache, and action cache.
        """
        self.current_balance = self.principal
        self.net_gain_loss = 0
        self.final_balance = 0
        self.strategy_investment_tracker = {}
        self.daily_data_cache = []
        self.action_cache = []
        return
    
    def clear_portfolio_strategies(self) -> None:
        """
        Clears all trading strategies associated with the portfolio.

        Empties the pre-market, mid-market, and post-market strategy lists.
        """
        self.pre_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        self.mid_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        self.post_market_strategies: List[Callable[['tickerPortfolio'], dict]] = []
        return

    def load_daily_data(self) -> None:
        """
        Loads and caches daily trading data for the portfolio's symbol.

        Fetches data for the current date and appends it to the daily data cache.
        
        Raises:
            FileNotFoundError: If daily data is not available.
        """
        try:
            data = dataHelp.load_data(self.symbol, '1m', dates.getDateXDaysFrom(0,self.date))
            for row in data.iterrows():
                self.daily_data_cache.append(row)
            print("Data Loaded")
            return
        except:
            raise FileNotFoundError("Daily Data not available")

    #TODO add ability to account for type of sale/purchase AKA limit sale/buy
    #add a type and price key to the tracker dictionary see if the price is > open? buy is possible if price is < open sell if possible
    #this seems lower in the prio since limit can be tracked in strategy? 
    #TODO add a way to make sure purchases are possible? maybe unsure here
    def load_live_data(self, data: pd.DataFrame) -> None:
        """
        Loads and processes live trading data, updating the portfolio's state accordingly.

        Appends the data to the daily data cache and adjusts the current balance
        based on the strategy investment tracker actions.

        Args:
            data (pd.DataFrame): The live data to be processed, expected to contain 
            columns with market data including 'Open' prices.

        Note:
            The function assumes all purchase and sale actions are possible if
            kept below 10% of the principal.
        """
        self.daily_data_cache.append(data)
        cur_price = data[1]['Open']
        time = data[0]
        #iterate through strat invest tracker
        #implement actions(update balances) and perform checks
        for name, strat in self.strategy_investment_tracker.items():
            act = strat['action']
            quant = strat['quantity']
            totes = strat['total']
            if act == 'buy':
                t_amount = quant*cur_price
                #we assume any purchase and sale is possible because the total volume should be kept less than 20% of prinicpal
                self.current_balance -= t_amount
                self.action_cache.append({'action': 'buy', 'amount': quant, 'time': time})
            elif act == 'sell':
                t_amount = quant*cur_price
                self.current_balance += t_amount
                self.action_cache.append({'action': 'sell', 'amount': quant, 'time': time})
            #action executed reset tracker
            self.strategy_investment_tracker[name] = {'action': None, 'quantity': 0, 'total': totes}

    #TODO Complete pre/post market implementation
    def pre_execute_strategies(self) -> None:
        """
        Executes all pre-market trading strategies and processes their results.

        Calls each pre-market strategy function and passes the portfolio instance.
        Aggregates results and processes them to update the strategy investment tracker.
        """
        action_list = []
        for strategy in self.pre_market_strategies:
            action_list.append(strategy(self))
        self.process_results(action_list)
        return
        
    def post_execute_strategies(self) -> None:
        """
        Executes all post-market trading strategies and processes their results.

        Calls each post-market strategy function and passes the portfolio instance.
        Aggregates results and processes them to update the strategy investment tracker.
        """
        action_list = []
        for strategy in self.post_market_strategies:
            action_list.append(strategy(self))
        self.process_results(action_list)
        return

    def mid_execute_strategies(self) -> None:
        """
        Executes all live (mid-market) trading strategies and processes their results.

        Calls each mid-market strategy function and passes the portfolio instance.
        Aggregates results and processes them to update the strategy investment tracker.
        """
        action_list = []
        for strategy in self.mid_market_strategies:
            action_list.append(strategy(self))
        self.process_results(action_list)
        return
            
    def process_results(self, action_list: List[dict]) -> None:
        """
        Processes the results from executed strategies and updates the strategy investment tracker.

        Iterates through each result in the action list, updating the investment tracker
        with the actions ('buy', 'sell', 'hold') and their quantities.

        Args:
            action_list (List[dict]): A list of strategy action results, where each
            result is a dictionary containing 'name', 'action', and 'quantity' keys.
        """
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
        return 

    def add_strategy(self, strategy: Callable[['tickerPortfolio'], dict], market_phase: Literal['pre', 'mid', 'post']) -> None:
        """
        Adds a trading strategy to the portfolio for a specified market phase.

        Args:
            strategy (Callable[['tickerPortfolio'], dict]): A callable strategy function 
            that takes a tickerPortfolio instance and returns an action dictionary.

            market_phase (Literal['pre', 'mid', 'post']): The phase of the market to which 
            the strategy should be added. Valid options are 'pre', 'mid', or 'post'.
        
        Raises:
            ValueError: If the market phase is not 'pre', 'mid', or 'post'.
        """
        if market_phase == 'pre':
            self.pre_market_strategies.append(strategy)
        elif market_phase == 'mid':
            self.mid_market_strategies.append(strategy)
        elif market_phase == 'post':
            self.post_market_strategies.append(strategy)
        else:
            raise ValueError("Invalid market phase. Choose from 'pre_market', 'mid_market', 'post_market'.")

    def save_to_file(self) -> None:
        """
        Saves the current state of the portfolio to a file.

        Ensures the directory structure exists and writes the portfolio object
        to a pickle file named after the symbol and date.

        Raises:
            ValueError: If the portfolio's symbol or date is not set.
        """
        print("Saving Portfolio: "+self.symbol+" " + self.date)
        if not self.symbol or not self.date:
            raise ValueError("Symbol and date must be set to save the strategy.")
        
        folder_path = os.path.join(tickerPortfolio.base_directory, self.symbol)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{self.date}.pkl")
        
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(symbol: str, date: str) -> 'tickerPortfolio':
        """
        Loads a portfolio from a file based on the symbol and date.

        Constructs the file path using the symbol and date, deserializes
        the portfolio object from the file, and returns it.

        Args:
            symbol (str): The symbol for which the portfolio is to be loaded.
            date (str): The date associated with the portfolio file.

        Returns:
            tickerPortfolio: The deserialized portfolio object.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
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

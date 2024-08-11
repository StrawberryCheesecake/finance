import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import pickle
from datetime import datetime as dt
from tickerPortfolio import tickerPortfolio  # Adjust the import path based on your project structure

class TestTickerPortfolio(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a sample tickerPortfolio instance."""
        self.symbol = 'AAPL'
        self.date = 'today'
        self.principal = 1000.0
        self.portfolio = tickerPortfolio(self.symbol, self.date, self.principal)

    @patch('src.tickerPortfolio.dates.getDateXDaysFrom')
    def test_init(self, mock_get_date):
        """Test initialization of tickerPortfolio with a valid symbol and date."""
        mock_get_date.return_value = self.date
        portfolio = tickerPortfolio('AAPL', 'today', 1000.0)
        
        self.assertEqual(portfolio.symbol, 'AAPL')
        self.assertEqual(portfolio.date, self.date)
        self.assertEqual(portfolio.principal, 1000.0)
        self.assertEqual(portfolio.current_balance, 1000.0)
        self.assertEqual(portfolio.net_gain_loss, 0)
        self.assertEqual(portfolio.final_balance, 0)
        self.assertIsInstance(portfolio.strategy_investment_tracker, dict)
        self.assertIsInstance(portfolio.daily_data_cache, list)
        self.assertIsInstance(portfolio.action_cache, list)
        
    def test_str(self):
        """Test the string representation of the tickerPortfolio."""
        tempDate = dt.today().strftime("%Y-%m-%d")
        expected_str = (
            f"TickerPortfolio(\n"
            f"  symbol={self.symbol},\n"
            f"  date={tempDate},\n"
            f"  principal={self.principal},\n"
            f"  current_balance={self.principal},\n"
            f"  net_gain_loss=0,\n"
            f"  final_balance=0,\n"
            f"  strategy_investment_tracker={self.portfolio._dict_summary(self.portfolio.strategy_investment_tracker)},\n"
            f"  daily_data_cache={self.portfolio._list_summary(self.portfolio.daily_data_cache)},\n"
            f"  action_cache={self.portfolio._list_summary(self.portfolio.action_cache)},\n"
            f"  pre_market_strategies={self.portfolio._strategy_summary(self.portfolio.pre_market_strategies)},\n"
            f"  mid_market_strategies={self.portfolio._strategy_summary(self.portfolio.mid_market_strategies)},\n"
            f"  post_market_strategies={self.portfolio._strategy_summary(self.portfolio.post_market_strategies)},\n"
            f"  historic_data_available={'Yes' if self.portfolio.historic_data else 'No'},\n"
            f"  previous_days_data_available={'Yes' if self.portfolio.previous_days_data else 'No'}\n"
            f")"
        )
        self.assertEqual(str(self.portfolio), expected_str)

    def test_clear_portfolio_data(self):
        """Test clearing portfolio data."""
        self.portfolio.current_balance = 500.0
        self.portfolio.net_gain_loss = 100.0
        self.portfolio.final_balance = 600.0
        self.portfolio.strategy_investment_tracker = {'test_strategy': {'action': 'buy', 'quantity': 10}}
        self.portfolio.daily_data_cache = [1, 2, 3]
        self.portfolio.action_cache = [4, 5, 6]
        
        self.portfolio.clear_portfolio_data()
        
        self.assertEqual(self.portfolio.current_balance, self.principal)
        self.assertEqual(self.portfolio.net_gain_loss, 0)
        self.assertEqual(self.portfolio.final_balance, 0)
        self.assertEqual(self.portfolio.strategy_investment_tracker, {})
        self.assertEqual(self.portfolio.daily_data_cache, [])
        self.assertEqual(self.portfolio.action_cache, [])

    def test_clear_portfolio_strategies(self):
        """Test clearing portfolio strategies."""
        strategy = lambda portfolio: {'name': 'test_strategy', 'action': 'buy', 'quantity': 10}
        self.portfolio.add_strategy(strategy, 'pre')
        self.portfolio.add_strategy(strategy, 'mid')
        self.portfolio.add_strategy(strategy, 'post')
        
        self.portfolio.clear_portfolio_strategies()
        
        self.assertEqual(len(self.portfolio.pre_market_strategies), 0)
        self.assertEqual(len(self.portfolio.mid_market_strategies), 0)
        self.assertEqual(len(self.portfolio.post_market_strategies), 0)

    @patch('src.tickerPortfolio.dataHelp.load_data')
    def test_load_daily_data(self, mock_load_data):
        """Test loading daily data into the portfolio."""
        mock_data = pd.DataFrame({'Open': [100, 101, 102]})
        mock_load_data.return_value = mock_data

        self.portfolio.load_daily_data()

        self.assertEqual(len(self.portfolio.daily_data_cache), len(mock_data))
        self.assertEqual(self.portfolio.daily_data_cache[-1], mock_data.iloc[-1])

    def test_add_strategy(self):
        """Test adding strategies to the portfolio."""
        strategy = lambda portfolio: {'name': 'test_strategy', 'action': 'buy', 'quantity': 10}

        self.portfolio.add_strategy(strategy, 'pre')
        self.portfolio.add_strategy(strategy, 'mid')
        self.portfolio.add_strategy(strategy, 'post')

        self.assertIn(strategy, self.portfolio.pre_market_strategies)
        self.assertIn(strategy, self.portfolio.mid_market_strategies)
        self.assertIn(strategy, self.portfolio.post_market_strategies)

        with self.assertRaises(ValueError):
            self.portfolio.add_strategy(strategy, 'invalid_phase')

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('pickle.dump')
    def test_save_to_file(self, mock_pickle_dump, mock_open, mock_makedirs):
        """Test saving the portfolio to a file."""
        self.portfolio.symbol = 'AAPL'
        self.portfolio.date = 'today'

        self.portfolio.save_to_file()

        expected_folder_path = os.path.join(tickerPortfolio.base_directory, self.portfolio.symbol)
        expected_file_path = os.path.join(expected_folder_path, f"{self.portfolio.date}.pkl")
        mock_makedirs.assert_called_with(expected_folder_path, exist_ok=True)
        mock_open.assert_called_with(expected_file_path, 'wb')
        mock_pickle_dump.assert_called_with(self.portfolio, mock_open())

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('pickle.load')
    @patch('os.path.exists', return_value=True)
    def test_load_from_file(self, mock_exists, mock_pickle_load, mock_open):
        """Test loading a portfolio from a file."""
        mock_pickle_load.return_value = self.portfolio

        loaded_portfolio = tickerPortfolio.load_from_file('AAPL', 'today')

        self.assertEqual(loaded_portfolio.symbol, self.portfolio.symbol)
        self.assertEqual(loaded_portfolio.date, self.portfolio.date)
        self.assertEqual(loaded_portfolio.principal, self.portfolio.principal)

    @patch('os.path.exists', return_value=False)
    def test_load_from_file_file_not_found(self, mock_exists):
        """Test loading a portfolio from a file that does not exist."""
        with self.assertRaises(FileNotFoundError):
            tickerPortfolio.load_from_file('AAPL', 'today')

if __name__ == '__main__':
    unittest.main()

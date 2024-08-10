from flask import Blueprint, jsonify, request
from src.portfolios.tickerPortfolio import tickerPortfolio as tp
from src.global_helpers import dataHelper
import json

manage_tick_bp = Blueprint('manage_tick', __name__)

@manage_tick_bp.route('/gettickport', methods=['POST'])
def get_ticker_portfolio():
    inputs = request.json
    symbol = inputs['symbol']
    date = inputs['date']
    principal = inputs['principal']
    if dataHelper.check_symbol_is_real(symbol):
        if dataHelper.check_tp_exists(symbol, date):
            tickerPort = tp.load_from_file(symbol, date)
            tickerPort.principal = principal
        else:
            tickerPort = tp(symbol, date, principal)
            tickerPort.load_daily_data()
    else:
        return "ERROR ERROR ERROR SYMBOL NOT REAL"
    
    return tickerPort.to_json()
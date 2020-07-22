from iexfinance.stocks import Stock
import redismanager
from main import normalize_data

"""
The official docs recommend using environment variable IEX_TOKEN
https://addisonlynch.github.io/iexfinance/stable/configuration.html#config-auth
"""

def get_quote(ticker):
    stonk = Stock(ticker)
    return stonk.get_price()

def trade_fee(cost):
    redismanager.trade_fee()
    cost = cost + 2
    return cost


def validate_funds_available(username, cost):
    balance = redismanager.get_user_cash_balance(username)
    if balance >= cost:
        return True
    else:
        return False


def validate_shares_available(username, ticker, amount):
    balance = redismanager.get_user_share_balance(username)
    for share in balance:
        if share[0].decode('utf-8') == ticker:
            if amount <= share[1]:
                return True
    return False


def execute_trade(username, cost, ticker, amount, value):
    try:
        redismanager.mod_user_balance(username, cost)
        redismanager.mod_share_balance(username, ticker, amount)
        redismanager.update_stock_cache_price(ticker, value)
        return None
    except Exception as e:
        print(e.message)
        return e.message


def get_shares(username):
    try:
        shares = redismanager.get_user_share_balance(username)
        return shares
    except Exception as e:
        print(e.message)
        return e.message


def update_stock_prices():
    stocks = redismanager.get_count_stocks_currently_held()
    stocks = normalize_data(stocks)
    for stock in stocks:
        currentprice = get_quote(stock[0])
        redismanager.update_stock_cache_price(stock[0], currentprice)

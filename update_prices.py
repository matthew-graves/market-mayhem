import redismanager
from trademanager import get_quote


def update_stock_prices():
    stocks = redismanager.get_stocks_currently_held()
    print(stocks)
    normalized_stocks = []
    for stock in stocks:
        stock = stock.decode("utf-8")
        normalized_stocks += [stock]
    batchstocks = tuple(normalized_stocks[n:n + 50] for n, i in enumerate(normalized_stocks)
                        if n % 50 == 0)
    for stock in batchstocks:
        currentprice = get_quote(stock)
        for ticker in currentprice:
            print(ticker, currentprice[ticker])
            redismanager.update_stock_cache_price(ticker, currentprice[ticker])


update_stock_prices()

import schedule
import time
import redismanager
import trademanager


def update_stock_prices():
    trademanager.update_stock_prices()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("Stock Prices Updated At: " + current_time)


def update_balances():
    redismanager.update_balances()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("Balances Updated At: " + current_time)


minutes = 0
hours = 6
minutetimes = []
hourtimes = []
scheduletimes = []

while minutes <= 55:
    minutetimes += [str(minutes).zfill(2)]
    minutes += 5


while hours <= 12:
    hourtimes += [str(hours).zfill(2)]
    hours += 1

for h in hourtimes:
    for m in minutetimes:
        scheduletimes += [h + ":" + m]
scheduletimes += ['13:00', '13:05']

for i in scheduletimes:
    schedule.every().monday.at(i).do(update_stock_prices)
    schedule.every().tuesday.at(i).do(update_stock_prices)
    schedule.every().wednesday.at(i).do(update_stock_prices)
    schedule.every().thursday.at(i).do(update_stock_prices)
    schedule.every().friday.at(i).do(update_stock_prices)


schedule.every(1).minutes.do(update_balances)


while 1:
    schedule.run_pending()
    time.sleep(1)

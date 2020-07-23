import redismanager
from trademanager import update_stock_prices
from datetime import datetime
from redismanager import update_balances
import time


now = datetime.now()
current_time = now.strftime("%m/%d/%y %H:%M:%S")

try:
	update_stock_prices()
	print("{0} | Prices Successfully Updated".format(current_time))
except Exception as e:
	print("{0} | Prices Failed To Update: {1}".format(current_time, e.msg))

now = datetime.now()
current_time = now.strftime("%m/%d/%y %H:%M:%S")

try:
        update_balances()
        print("{0} | Balances Successfully Updated".format(current_time))
except Exception as e:
        print("{0} | Balances Failed To Update: {1}".format(current_time, e.msg))

now = datetime.now()
current_time = now.strftime("%m/%d/%y %H:%M:%S")

time.sleep(15)

try:
        update_balances()
        print("{0} | Balances Successfully Updated".format(current_time))
except Exception as e:
        print("{0} | Balances Failed To Update: {1}".format(current_time, e.msg))

now = datetime.now()
current_time = now.strftime("%m/%d/%y %H:%M:%S")

time.sleep(15)
try:
        update_balances()
        print("{0} | Balances Successfully Updated".format(current_time))
except Exception as e:
        print("{0} | Balances Failed To Update: {1}".format(current_time, e.msg))

now = datetime.now()
current_time = now.strftime("%m/%d/%y %H:%M:%S")

time.sleep(15)
try:
        update_balances()
        print("{0} | Balances Successfully Updated".format(current_time))
except Exception as e:
        print("{0} | Balances Failed To Update: {1}".format(current_time, e.msg))

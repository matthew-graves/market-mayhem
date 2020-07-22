import redismanager
import trademanager
import time
#
import random
import numpy as np

# start_time = time.time()
# leaders = redismanager.get_leaders(-1)
# print("--- %s seconds ---" % (time.time() - start_time))
#
# start_time = time.time()
# for leader in leaders:
#     print(redismanager.get_user_balance(leader[0].decode("utf-8")))
#     print(redismanager.get_share_balance(leader[0].decode("utf-8")))
# print("--- %s seconds ---" % (time.time() - start_time))


def seed_database(usercount):
    import grequests
    count = 0
    urls = []
    usernames = np.random.randint(1, 10000000, usercount)
    for username in usernames:
        uri = "http://localhost:8000/api/users/" + str(username)
        urls += [uri]
    print("starting request")
    print(urls)
    rs = (grequests.get(u) for u in urls)
    grequests.map(rs, size=100)
    return "users added"


def seed_stocks(usercount):
    users = redismanager.get_users(usercount)
    for user in users:
        user = user[0].decode('utf-8')
        amounttobuy = random.randint(1, 5)
        stockchoice = random.choice(["AAPL", "TSLA", "MSFT", "MVIS", "F", "NKLA"])
        print(stockchoice)
        value = trademanager.get_quote(stockchoice)
        cost = value * amounttobuy
        print(user)
        trademanager.execute_trade(user, cost, stockchoice, amounttobuy, value)

# seed_database(10000)
# seed_stocks(1000)

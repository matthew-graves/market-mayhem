from usermanager import User, create_user
import redis
import os


class RedisGenericException(Exception):
    pass


def get_ranking(username):
    validate_online()
    user = r.zrevrank("balances", username)
    if user is None:
        return "User has not traded yet, start trading to get ranked!"
    else:
        return user+1


def validate_user_exists(username):
    validate_online()
    user = r.zscore("balances", username)
    if user is None:
        user = create_user(username)
        r.zadd("balances", {username: user.balance})
    else:
        return True


def get_user_cash_balance(username):
    validate_online()
    user = r.zscore("balances", username)
    if user is None:
        user = create_user(username)
        r.zadd("balances", {username: user.balance})
        return user.balance
    else:
        return user


def get_user_account_value(username):
    validate_online()
    user = r.zscore("accountvalue", username)
    if user is None:
        user = create_user(username)
        r.zadd("accountvalue", {username: user.balance})
        return user.balance
    else:
        return user


def mod_user_balance(username, balancemod):
    validate_online()
    user = r.zscore("balances", username)
    if user is None:
        user = create_user(username)
        r.zadd("balances", {username: user.balance})
        r.zincrby("balances", -balancemod, username)
        user = r.zscore("balances", username)
        return user
    else:
        r.zincrby("balances", -balancemod, username)
        user = r.zscore("balances", username)
        return user


def mod_share_balance(username, ticker, amount):
    validate_online()
    # Update User's Share Count
    r.zincrby(username, amount, ticker)
    # Delete Key to Save Memory If Number of Shares is Zero After Modification
    if r.zscore(username, ticker) == 0:
        r.zrem(username, ticker)

    # Update Total Count of Shares
    r.zincrby("activestocks", amount, ticker)
    if r.zscore("activestocks", ticker) == 0:
        r.zrem("activestocks", ticker)
        r.zrem("stockprices", ticker)
    return None


def get_user_share_balance(username):
    validate_online()
    shares = r.zrange(username, 0, -1, withscores=True)
    return shares


def get_users(users):
    validate_online()
    return r.zrevrange("balances", 0, users, withscores=True)


def get_leaders(leaders):
    validate_online()
    return r.zrevrange("accountvalue", 0, leaders, withscores=True)


def get_losers(losers):
    validate_online()
    return r.zrange("accountvalue", 0, losers, withscores=True)


def trade_fee():
    validate_online()
    return r.zincrby("stats", 2, "tradefees")


def get_stock_price_cache():
    validate_online()
    shares = r.zrange("stockprices", 0, -1, withscores=True)
    return shares


def update_stock_cache_price(stock, price):
    validate_online()
    r.zadd("stockprices", {stock: price})
    return None


def get_stocks_currently_held():
    validate_online()
    stocks = r.zrange("activestocks", 0, -1, withscores=True)
    return stocks


def update_balances():
    validate_online()
    users = get_users(-1)
    for user in users:
        accountvalue = 0
        user = user[0].decode('utf-8')
        shares = get_user_share_balance(user)
        if shares:
            for share in shares:
                sharename = share[0].decode('utf-8')
                sharequantity = share[1]
                accountvalue += sharequantity * r.zscore("stockprices", sharename)

        accountvalue += r.zscore("balances", user)
        r.zadd("accountvalue", {user: accountvalue})


def update_stats_user_count():
    validate_online()
    usercount = r.zcount("balances", "-inf", "inf")
    r.zadd("stats", {"usercount": usercount})


def update_stats_total_unique_companies():
    validate_online()
    companycount = r.zcount("activestocks", "-inf", "inf")
    r.zadd("stats", {"unique companies": companycount})


def get_mayhem_value():
    validate_online()
    stocks = r.zrange("activestocks", 0, -1, withscores=True)
    stockprices = r.zrange("stockprices", 0, -1, withscores=True)
    totalvalue = 0
    for stock in stocks:
        price = list(filter(lambda x:stock[0] in x, stockprices))
        totalvalue += (stock[1] * price[0][1])
    return totalvalue


def get_usage_stats():
    validate_online()
    return r.zrange("stats", 0, -1, withscores=True)


def get_leader_stats():
    validate_online()
    username = r.zrevrange("accountvalue", 0, 0, withscores=True)
    username = username[0]
    cash_value = r.zscore("balances", username[0])
    share_count = r.zcount(username[0], "-inf", "inf")
    stats = [username[0].decode("utf-8"), cash_value, (username[1] - cash_value), share_count, username[1]]
    return stats


def get_loser_stats():
    validate_online()
    username = r.zrange("accountvalue", 0, 0, withscores=True)
    username = username[0]
    cash_value = r.zscore("balances", username[0])
    share_count = r.zcount(username[0], "-inf", "inf")
    stats = [username[0].decode("utf-8"), cash_value, (username[1] - cash_value), share_count, username[1]]
    return stats


# Private functions


def validate_online():
    global r

    if r is None:
        return establish_connection()

    try:
        r.ping()
        return r
    except Exception as e:
        try:
            open_redis_with_env()
            return establish_connection()
        except Exception as e:
            raise RedisGenericException("Database Is Offline")


def open_redis_with_env():
    host = os.getenv('REDIS_HOST', 'localhost')
    return redis.Redis(host=host)


def establish_connection():
    global r
    r = open_redis_with_env()
    r.config_set("save", "600 1")
    return r


r = None
r = validate_online()

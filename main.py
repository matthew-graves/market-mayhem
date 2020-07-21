import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
import redismanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import trademanager

app = FastAPI(openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def normalize_data(redisarray):
    processedarray = []
    for item in redisarray:
        processedarray += [(item[0].decode("utf-8"), round(item[1], 2))]
    return processedarray


@app.get("/api/users/{username}/cash")
async def users(request: Request, username: str):
    username = username.upper()
    try:
        return redismanager.get_user_cash_balance(username)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/users/{username}")
async def users(request: Request, username: str):
    username = username.upper()
    try:
        sharevalues = []
        cash = redismanager.get_user_cash_balance(username)
        shares = redismanager.get_user_share_balance(username)
        total = redismanager.get_user_account_value(username)
        shares = normalize_data(shares)
        allsharevalues = redismanager.get_stock_price_cache()
        allsharevalues = normalize_data(allsharevalues)
        for share in shares:
            for sharevalue in allsharevalues:
                if share[0] == sharevalue[0]:
                    sharevalues += [sharevalue]
        print(sharevalues)
        return templates.TemplateResponse("userinfo.html", {"cash": cash, "shares": shares, "total": total, "request": request, "sharevalues": sharevalues})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/stats")
async def users(request: Request):
    try:
        redismanager.update_stats_total_unique_companies()
        redismanager.update_stats_user_count()
        stats = redismanager.get_usage_stats()
        return normalize_data(stats)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/update_scores")
async def users(request: Request):
    try:
        trademanager.update_stock_prices()
        redismanager.update_balances()
        return True
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/users/{username}/shares")
async def users(request: Request, username: str):
    username = username.upper()
    try:
        return trademanager.get_shares(username)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/stock/{ticker}")
async def users(request: Request, ticker: str):
    ticker = ticker.upper()
    try:
        return trademanager.get_quote(ticker)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/stock/{ticker}/buy/{amount}/user/{username}")
async def users(request: Request, ticker: str, amount: int, username: str):
    username = username.upper()
    ticker = ticker.upper()
    ticker = ticker[1:] if ticker.startswith("$") else ticker
    if amount < 1:
        return "Positive Numbers Only ;)"
    try:
        redismanager.validate_user_exists(username)
        value = trademanager.get_quote(ticker)
        cost = value
        cost *= amount
        if trademanager.validate_funds_available(username, cost):
            cost = trademanager.trade_fee(cost)
            success = trademanager.execute_trade(username, cost, ticker, amount, value)
            if success is None:
                return "Trade Successful"
            else:
                return success
        else:
            return "Insufficient Funds (that happened last time!?!?)"
    except Exception as e:
        return "An error occurred processing your request, please validate that you entered a valid ticker"
        # return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/stock/{ticker}/sell/{amount}/user/{username}")
async def users(request: Request, ticker: str, amount: int, username: str):
    username = username.upper()
    ticker = ticker.upper()
    ticker = ticker[1:] if ticker.startswith("$") else ticker
    if amount < 1:
        return "Positive Numbers Only ;)"
    try:
        redismanager.validate_user_exists(username)
        value = trademanager.get_quote(ticker)
        cost = value
        cost *= amount
        cost = -cost
        if trademanager.validate_shares_available(username, ticker, amount):
            amount = -amount
            success = trademanager.execute_trade(username, cost, ticker, amount, value)
            if success is None:
                return "Trade Successful"
            else:
                return success
        else:
            return "You do not have " + str(amount) + " shares of $" + ticker + " to sell"
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/ranking/{username}")
async def users(request: Request, username: str):
    username = username.upper()
    try:
        return redismanager.get_ranking(username)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/api/balance/{username}/{balancemod}")
async def users(request: Request, username: str, balancemod: float):
    username = username.upper()
    try:
        return redismanager.mod_user_balance(username, balancemod)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})


@app.get("/top/{leaders}")
async def generate_leaderboard(request: Request, leaders: int):
    try:
        leaders = redismanager.get_leaders(int(leaders) - 1)
        processedleaders = normalize_data(leaders)
        return templates.TemplateResponse("leaderboard.html", {"leaders": processedleaders, "request": request})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})

@app.get("/")
async def generate_leaderboard(request: Request):
    try:
        leaders = redismanager.get_leaders(24)
        processedleaders = normalize_data(leaders)
        return templates.TemplateResponse("leaderboard.html", {"leaders": processedleaders, "request": request})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"error": e, "request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
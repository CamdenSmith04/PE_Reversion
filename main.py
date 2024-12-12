import robin_stocks.robinhood as r
import pandas as pd

# Get user login information to access api
file = open(".password.txt", "r")
username = file.readline()[:-1]
password = file.readline()[:-1]
r.login(username, password)
print("Sign in successful.")

# Industry Specific Stocks
steel = ["STLD", "NUE", "CLF", "X"]
materials = []

# Collection of ETFs
etfs = ["XLB", "SLX"]

# Collection of Stocks
stocks = []
for i in range(len(steel)):
    stocks.append(steel[i])

# Function to get the P/E ratio of a stock
def get_PE(stock):
    return r.get_fundamentals(stock, info="pe_ratio")


print(r.stocks.get_stock_historicals("STLD",interval="day",span="year",bounds="regular",info="close_price"))

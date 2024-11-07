import robin_stocks.robinhood as r
import pandas as pd

# Get user login information to access api
file = open(".password.txt", "r")
username = file.readline()[:-1]
password = file.readline()[:-1]
r.login(username, password)

# Industry Specific Stocks
steel = ["STLD", "NUE", "CLF", "X"]



# Collective Stocks
stocks = []

for i in range(len(steel)):
    stocks.append(steel[i])

print(stocks)








print("Done")
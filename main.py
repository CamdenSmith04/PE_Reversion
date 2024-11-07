import robin_stocks.robinhood as r
import pandas as pd

# Get user login information to access api
file = open(".password.txt", "r")
username = file.readline()
username = username[0:-1]

password = file.readline()
password = password[0:-1]

r.login(username, password)

print("Done")
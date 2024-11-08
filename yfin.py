# %%
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker_symbol = "STLD"
stock = yf.Ticker(ticker_symbol)

price_data = stock.history(period="max")['Close']
price_data.index = pd.to_datetime(price_data.index).tz_localize(None)

financials = stock.financials
shares_outstanding = stock.info.get("sharesOutstanding")

eps_data = (financials.loc['Basic EPS'])
eps_data.index = pd.to_datetime(eps_data.index).tz_localize(None)

pe_ratios = pd.DataFrame(index=price_data.index, columns=["P/E Ratio"])

for date, price in price_data.items():
    past_eps = eps_data[eps_data.index <= date]
    if not past_eps.empty:
        latest_eps = past_eps.iloc[0]
        pe_ratios.loc[date] = price / latest_eps if latest_eps != 0 else None

pe_ratios.dropna(inplace=True)


plt.figure(figsize=(10,6))
plt.plot(pe_ratios.index, pe_ratios['P/E Ratio'], label=f"{ticker_symbol} P/E Ratio", color='blue')

plt.title(f"{ticker_symbol} Quarterly P/E Ratio")
plt.xlabel('Date')
plt.ylabel('P/E Ratio')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()

plt.show()
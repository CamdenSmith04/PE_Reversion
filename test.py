import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the stock ticker
ticker_symbol = "AAPL"  # Example: Apple Inc.
stock = yf.Ticker(ticker_symbol)

# Step 1: Download historical price data
price_data = stock.history(period="5y")['Close']  # Get the last 5 years of closing prices
price_data.index = pd.to_datetime(price_data.index).tz_localize(None)  # Ensure timezone-naive datetime format

# Step 2: Get quarterly net income from financials and calculate approximate TTM EPS
financials = stock.quarterly_financials  # Get quarterly financial statements
shares_outstanding = stock.info.get("sharesOutstanding")  # Get current shares outstanding

if financials.empty or shares_outstanding is None:
    print("Quarterly financial data or shares outstanding data is not available.")
else:
    # Get net income for the last 4 quarters
    net_income = financials.loc['Net Income']
    net_income.index = pd.to_datetime(net_income.index).tz_localize(None)  # Ensure timezone-naive datetime format

    # Step 3: Calculate TTM Net Income by summing the last 4 quarters
    ttm_net_income = net_income.rolling(window=4).sum()  # Sum of last 4 quarters for TTM
    ttm_net_income = ttm_net_income.dropna()  # Drop NaN values (for the first 3 periods)

    # Step 4: Calculate TTM EPS (Net Income / Shares Outstanding)
    ttm_eps = ttm_net_income / shares_outstanding

    # Step 5: Calculate P/E ratio by aligning price with TTM EPS
    pe_ratios = pd.DataFrame(index=price_data.index, columns=["P/E Ratio"])

    for date, price in price_data.items():
        # Find the most recent TTM EPS before the price date
        past_ttm_eps = ttm_eps[ttm_eps.index <= date]
        if not past_ttm_eps.empty:
            latest_ttm_eps = past_ttm_eps.iloc[-1]  # Get the latest TTM EPS before the date
            pe_ratios.loc[date] = price / latest_ttm_eps if latest_ttm_eps != 0 else None

    # Drop any rows with missing values
    pe_ratios.dropna(inplace=True)

    # Step 6: Plot the P/E ratio
    plt.figure(figsize=(10, 6))
    plt.plot(pe_ratios.index, pe_ratios['P/E Ratio'], label=f'{ticker_symbol} P/E Ratio', color='blue')
    
    # Customize the plot
    plt.title(f'{ticker_symbol} Trailing Twelve Months (TTM) P/E Ratio')
    plt.xlabel('Date')
    plt.ylabel('P/E Ratio')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.show()

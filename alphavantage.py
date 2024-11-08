import requests
import matplotlib.pyplot as plt

API_KEY = 'HW6QXOX01KKV3UPC'
ticker_symbol = 'AAPL'

# Step 2: Get Weekly Stock Prices (for the last 5 years)
price_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker_symbol}&apikey={API_KEY}"
price_response = requests.get(price_url)
price_data = price_response.json()

# Step 3: Debugging Step - Print the raw price data
print(price_data)

# Check if "Weekly Time Series" exists in the response
if 'Weekly Time Series' not in price_data:
    print("Error: Weekly stock price data not available.")
    exit()

# Get stock prices for the last 5 years (weekly data)
closing_prices = []
for date, data in price_data['Weekly Time Series'].items():
    closing_prices.append((date, float(data['4. close'])))  # Ensure price is a float

# Step 4: Get Earnings Data (EPS) for the past 5 years
earnings_url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker_symbol}&apikey={API_KEY}"
earnings_response = requests.get(earnings_url)
earnings_data = earnings_response.json()
annual_earnings = earnings_data.get('annualEarnings', [])

# Filter the earnings data to get the last 5 years
earnings_data_filtered = annual_earnings[:5]

# Step 5: Calculate P/E Ratio for each year
pe_ratios = []
for (fiscal_date, closing_price), earnings in zip(closing_prices, earnings_data_filtered):
    eps = float(earnings['reportedEPS'])  # Ensure EPS is a float
    
    # Calculate P/E Ratio: Price / EPS
    if eps != 0:
        pe_ratio = closing_price / eps
        pe_ratios.append((fiscal_date, pe_ratio))

# Step 6: Plot the P/E Ratios
years = [fiscal_date[:4] for fiscal_date, _ in pe_ratios]
pe_values = [pe for _, pe in pe_ratios]

plt.plot(years, pe_values, marker='o')
plt.title(f"{ticker_symbol} 5-Year P/E Ratio (Weekly Data)")
plt.xlabel("Year")
plt.ylabel("P/E Ratio")
plt.grid(True)
plt.show()

# Print the results
for year, pe in zip(years, pe_values):
    print(f"Year: {year} - P/E Ratio: {pe}")

#api key 6OTO8B7B86VTLIY4 alpha vantage
import yfinance as yfin
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=6OTO8B7B86VTLIY4'
r = requests.get(url)
data = r.json()

print((data["Time Series (Daily)"]["2020-01-21"]))

GetFacebookInformation = yfin.Ticker("META")
 
# Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y,
# 2y, 5y, 10y and ytd.
print(GetFacebookInformation.history(period="6mo"))

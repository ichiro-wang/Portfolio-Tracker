import requests
from InvalidAction import StockNotFound
from Constants import AV_API_KEY

def get_data(ticker):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    #     f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey={API_KEY}"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={AV_API_KEY}"
    r = requests.get(url)
    data = r.json()

    return data

def get_price(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={AV_API_KEY}"
    r = requests.get(url)
    data = r.json()

    data_keys = list(data.keys())
    if data_keys[0] == "Error Message":
        raise StockNotFound(data["Error Message"])
    elif data_keys[0] == "Meta Data":
        first_day = next(iter(data["Time Series (Daily)"]))
        price_close = data["Time Series (Daily)"][first_day]["4. close"]
        price_close = float(price_close)
        return price_close
    else:
        raise Exception("Error pertaining to API call.")

def main():
    price = get_price("AAPL")
    print(f"${price:,.2f}")

if __name__ == "__main__":
    main()
import requests
from InvalidAction import StockNotFound
from Constants import get_key
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("stockdata.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_data(ticker):
    url = (f"https://www.alphavantage.co/query?function"
           f"=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={get_key()}")
    r = requests.get(url)
    data = r.json()

    return data

def get_price(ticker):

    logging.info(f"Retrieving stock price for {ticker}")

    test_values = {"AAPL":226.78, "GOOGL":165.86, "TSLA":249.02, "VFV.TRT":136.60}

    if ticker in test_values:
        return test_values[ticker]

    logging.info(f"Calling API for {ticker}")
    data = get_data(ticker)
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
    ticker = "VFV.TO"
    if ".TO" in ticker:
        ticker = ticker.split(".")[0]
        ticker += ".TRT"
        price = get_price(ticker)
        print(f"${price:,.2f}")

    price = get_price("GOOGL")
    print(f"${price:,.2f}")
    price = get_price("AAPL")
    print(f"${price:,.2f}")
    price = get_price("TSLA")
    print(f"${price:,.2f}")


if __name__ == "__main__":
    main()
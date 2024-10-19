import requests
from InvalidAction import StockNotFound
import Constants
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("logs/stockdata.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


cad_to_usd_rate = 0.72
# cad_to_usd_rate = 0.5

def cad_to_usd(cad: float) -> float:
    return cad * cad_to_usd_rate

def usd_to_cad(usd: float) -> float:
    return usd / cad_to_usd_rate

def get_data(ticker):
    url = f"https://www.alphavantage.co/query"

    parameters = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": Constants.get_av_key()
    }

    r = requests.get(url, params=parameters)
    return r.json()

def get_price(ticker) -> float:

    # test_values = {"TEST":100}
    test_values = {"AAPL":235, "GOOGL":163.42, "TSLA":249.02, "VFV.TRT":136.60, "TEST":100}
    if ticker in test_values:
        logger.info(f"Retrieving default price for {ticker}")
        return test_values[ticker]

    logger.info(f"Calling API for {ticker}")
    data = get_data(ticker)
    if data["Global Quote"]:
        return float(data["Global Quote"]["05. price"])
    else:
        raise StockNotFound(f"{ticker} was not found.")

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
    try:
        print(get_price("AMZN"))
        print(get_price("AMZNNNN"))
    except StockNotFound as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
import requests

# from requests import Session
# from requests.adapters import HTTPAdapter
# from urllib3.util import Retry

from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

# s = Session()
# retries = Retry(
#     total=3,
#     backoff_factor=0.1,
#     status_forcelist=[502, 503, 504],
# )
# s.mount("https://", HTTPAdapter(max_retries=retries))


def get_stock_details(ticker: str):
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": os.getenv("STOCK_API_KEY"),
        }

        res = requests.get(url=url, params=params)

        if not res.ok:
            raise Exception("Error retrieving stock api data")

        data = res.json()
        global_quote = data.get("Global Quote", None)
        if not global_quote:
            raise Exception("Error retrieving stock api data")

        price = float(global_quote["05. price"])
        change = float(global_quote["09. change"])
        change_percent = float(global_quote["10. change percent"].strip("%"))

        return {"price": price, "change": change, "change_percent": change_percent}

    except Exception as e:
        print("error in get_stock_details", e)
        return {"error": str(e)}

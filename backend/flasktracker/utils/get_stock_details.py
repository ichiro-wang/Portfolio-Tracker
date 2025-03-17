import requests
from dotenv import load_dotenv
import os

load_dotenv()


# helper function to make call to third party stock api
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

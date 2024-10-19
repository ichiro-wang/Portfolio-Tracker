from datetime import datetime

import Date
import StockData
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("logs/stock.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Stock:

    def __init__(self, ticker: str, currency="", comment="") -> None:
        self.ticker: str = ticker.upper()  # ticker symbol
        self.comment: str = comment  # save any comments
        self.qty_open: float = 0  # how many shares currently owned
        self.qty_closed: float = 0  # how many shares sold
        self.value_book: float = 0  # how much the shares were bought for (sum)
        self.price_mkt_cached: dict[str, datetime | float] = {}

        # how many bought historically, how much that costed, and the avg price of the stock when bought
        self.qty_total: float = 0  # how many shares bought in total
        self.value_total: float = 0  # how much spent buying total shares
        # self.price_avg_buy: float = 0  # avg stock price when bought shares

        self.value_book_sell: float = 0 # total value of sold shares
        self.price_avg_sell: float = 0 # avg price of sold shares

        logger.info(f"Created Stock {ticker}")

    @property
    def price_avg_buy(self):
        if self.qty_total == 0:
            return 0
        return self.value_total / self.qty_total

    # save current market price to prevent repeated api calls
    # if the market price is not updated to today, then call api
    def price_mkt_update(self):
        if not self.price_mkt_cached or not Date.within_last_hour(self.price_mkt_cached["date"]):
            logger.info("updating stock price")
            self.price_mkt_cached["date"] = datetime.now()
            self.price_mkt_cached["price"] = StockData.get_price(self.ticker)

    @property
    def price_mkt(self):
        self.price_mkt_update()
        return self.price_mkt_cached["price"]

    @property
    def value_mkt(self):
        return self.price_mkt * self.qty_open

    @property
    def open_pl(self):
        return self.value_mkt - self.value_book

    @property
    def open_pl_percent(self):
        if self.value_book == 0:
            return "0.00%"
        return f"{self.open_pl / self.value_book * 100 :,.2f}%"

    @property
    def close_pl(self):
        return self.value_book_sell

    @property
    def close_pl_percent(self):
        if self.value_book_sell == 0:
            return "0.00%"
        return f"{self.close_pl / (self.qty_closed * self.price_avg_buy) * 100 :,.2f}%"

    @staticmethod
    def currency(ticker: str) -> str:
        if ".TRT" in ticker:
            return "CAD"
        elif "." not in ticker:
            return "USD"

    def adjust_stats(self, transaction: str, qty: float, price: float) -> None:
        transaction = transaction.upper()
        if transaction == "BUY":
            self.qty_open += qty
            self.value_book += (qty * price)
            self.qty_total += qty
            self.value_total += (qty * price)
        elif transaction == "SELL":
            self.qty_open = self.qty_open - qty
            self.qty_closed += qty
            self.value_book -= (qty * self.price_avg_buy)
            self.value_book_sell += qty * (price - self.price_avg_buy)
            self.price_avg_sell = self.value_book_sell / self.qty_closed

    @staticmethod
    def header_str():
        return (f"""{"Ticker":.<8}{"Open Qty":.<10}{"Closed Qty":.<12}{"Avg Price":.<14}{"Mkt Price":.<14}"""
                f"""{"Book Value":.<16}{"Mkt Value":.<15}{"Open P&L":.<14}{"% Open P&L":.<14}"""
                f"""{"Closed P&L":.<14}{"% Closed P&L":.<12}""")

    def __str__(self) -> str:
        string = (f"{self.ticker:<8}{self.qty_open:<10}{self.qty_closed:<12}${self.price_avg_buy:<13,.1f}"
                  f"${self.price_mkt:<13,.2f}${self.value_book:<15,.2f}${self.value_mkt:<14,.2f}"
                  f"${self.open_pl:<13,.2f}{self.open_pl_percent:<14}${self.close_pl:<13,.2f}{self.close_pl_percent}")

        return string

    # repr of stock object
    # def __repr__(self) -> str:
    #     represent = (f"Details for {self.ticker}:\nOpen Qty: {self.qty_open}, Avg Price: ${self.price_avg_buy:,.2f}, "
    #                  f"Book Value: ${self.value_book:,.2f}" if self.value_book >= 0
    #                   else f"Book Value: -${-self.value_book:,.2f}")
    #
    #     return represent


def main():
    stock = Stock("TSLA", "elon musk")

    print(Stock.header_str())
    print(stock)
    print(stock)
    print(stock)
    print(stock)


if __name__ == "__main__":
    main()
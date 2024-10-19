import logging
from datetime import datetime

import StockData
from InvalidAction import InsufficientShares
from Stock import Stock

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("logs/portfolio.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class Portfolio:
    def __init__(self):
        # track stock portfolio
        # key: ticker, value: Stock object
        self.stocks: dict[str, Stock] = {}

        # date: datetime, str, ticker: str, qty: float, price: float, fees: float
        self.history_buy: list[dict[str, datetime | str | float]] = []
        self.history_sell: list[dict[str, datetime | str | float]] = []

    @property
    def value_book_total(self) -> float:
        return sum(StockData.usd_to_cad(stock.value_book) if Stock.currency(stock.ticker) == "USD" else stock.value_book
                   for stock in self.stocks.values())

    @property
    def value_mkt_total(self) -> float:
        return sum(StockData.usd_to_cad(stock.value_mkt) if Stock.currency(stock.ticker) == "USD" else stock.value_mkt
                   for stock in self.stocks.values())

    # buying a stock
    def buy(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        # if not in portfolio, add the new stock to the portfolio
        if ticker not in self.stocks:
            stock_buying = Stock(ticker)
            self.stocks[ticker] = stock_buying
        else:
            stock_buying = self.stocks[ticker]

        # performing required calculations for buying a stock
        stock_buying.adjust_stats("BUY", qty, price)
        self.history_buy.append({"date": date, "ticker": ticker, "qty": qty, "price": price, "fee": fee})

    # selling a stock
    # precondition: must own sufficient shares to sell
    def sell(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        # check if stock is owned
        if ticker not in self.stocks:
            raise InsufficientShares(f"Cannot sell {ticker} as you do not own any shares. "
                                     f"Transaction not accepted.")

        # get stock object that we are selling
        stock_selling = self.stocks[ticker]

        # check if sufficient shares owned
        if stock_selling.qty_open - qty < 0:
            raise InsufficientShares(f"Cannot sell {ticker} as you do not own sufficient shares. "
                                     f"Transaction not accepted.")

        # performing required calculations for selling stock
        stock_selling.adjust_stats("SELL", qty, price)
        self.history_sell.append({"date": date, "ticker": ticker, "qty": qty, "price": price, "fee": fee})

    # return portfolio info as string
    def get_portfolio(self) -> str:
        if self.stocks:
            return "\n".join(str(stock) for stock in self.stocks.values())
        else:
            logger.warning("No portfolio")
            return "Empty portfolio"

    def get_history(self, transaction: str) -> str:
        transaction = transaction.lower()
        if transaction == "buy":
            history = self.history_buy
        elif transaction == "sell":
            history = self.history_sell
        else:
            return "Cannot retrieve history"

        if history:
            return "\n".join(
                f"{h['date'].strftime('%Y-%m-%d')}, {h['ticker']}, {h['qty']}, "
                f"{h['price']}, {h['fee']}" for h in history)
        else:
            msg = f"No {transaction} history"
            logger.warning(msg)
            return msg

    def __str__(self) -> str:
        represent = f"\n{Stock.header_str()}"
        if self.stocks:
            represent += "\n" + self.get_portfolio()
        if self.history_buy:
            represent += "\nBuy History"
            represent += "\n" + self.get_history("buy")
        if self.history_sell:
            represent += "\nSell History"
            represent += "\n" + self.get_history("sell")

        return represent
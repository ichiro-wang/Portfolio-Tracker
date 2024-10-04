import logging
from datetime import datetime

from InvalidAction import InsufficientBalance, InsufficientShares
from Stock import Stock

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("portfolio.log")
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
        self.history_buy: list[tuple[datetime, str, float, float, float]] = []
        self.history_sell: list[tuple[datetime, str, float, float, float]] = []

    # buying a stock
    def buy(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        # if not in portfolio, add the new stock to the portfolio
        if ticker not in self.stocks:
            buy_stock = Stock(ticker)
            self.stocks[ticker] = buy_stock
        else:
            buy_stock = self.stocks[ticker]

        # performing required calculations for buying a stock
        buy_stock.qty_open += qty
        buy_stock.value_book += (qty * price)
        buy_stock.qty_total += qty
        buy_stock.value_total += (qty * price)
        self.history_buy.append((date, ticker, qty, price, fee))


    # selling a stock
    # precondition: must own sufficient shares to sell
    def sell(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        # check if stock is owned
        if ticker not in self.stocks:
            raise InsufficientShares(f"Cannot sell {ticker} as you do not own any shares. "
                                     f"Transaction not accepted.")

        # get stock object that we are selling
        sell_stock = self.stocks[ticker]

        qty_remain = sell_stock.qty_open - qty
        # check if sufficient shares owned
        if qty_remain < 0:
            raise InsufficientShares(f"Cannot sell {ticker} as you do not own sufficient shares. "
                                     f"Transaction not accepted.")

        # performing required calculations for selling stock
        sell_stock.qty_open = qty_remain
        sell_stock.qty_closed += qty
        sell_stock.value_book -= (qty * sell_stock.price_avg_buy)
        sell_stock.value_book_sell += qty * (price - sell_stock.price_avg_buy)
        sell_stock.price_avg_sell = sell_stock.value_book_sell / sell_stock.qty_closed
        self.history_sell.append((date, ticker, qty, price, fee))

    # return portfolio info as string
    def get_portfolio(self) -> str:
        if self.stocks:
            return "\n".join(str(stock) for stock in self.stocks.values())
        else:
            logger.warning("No portfolio")
            return "Empty portfolio"

    def get_history_buy(self) -> str:
        if self.history_buy:
            return "\n".join(f"{b[0].strftime('%Y-%m-%d')}, {b[1]}, {b[2]}, {b[3]}, {b[4]}" for b in self.history_buy)
        else:
            msg = "No buy history"
            logger.warning(msg)
            return msg

    def get_history_sell(self) -> str:
        if self.history_sell:
            return "\n".join(f"{w[0].strftime('%Y-%m-%d')}, {w[1]}, {w[2]}, {w[3]}, {w[4]}" for w in self.history_sell)
        else:
            msg = "No sell history"
            logger.warning(msg)
            return msg
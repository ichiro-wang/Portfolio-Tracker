import logging
from datetime import datetime

from InvalidAction import InsufficientShares
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
            stock_buying = Stock(ticker)
            self.stocks[ticker] = stock_buying
        else:
            stock_buying = self.stocks[ticker]

        # performing required calculations for buying a stock
        stock_buying.buy(qty, price)
        self.history_buy.append((date, ticker, qty, price, fee))


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
        stock_selling.sell(qty, price)
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

    def __str__(self) -> str:
        represent = f"\n{Stock.header_str()}"
        if self.stocks:
            represent += self.get_portfolio() + "\n"
        if self.history_buy:
            represent += "Buy History\n"
            represent += self.get_history_buy() + "\n"
        if self.history_sell:
            represent += "Sell History\n"
            represent += self.get_history_sell() + "\n"

        return represent
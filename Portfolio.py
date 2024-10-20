import logging
from datetime import datetime
from collections import deque
import Date
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

# helper method for keeping history sorted
def history_insert_index(date: datetime, history: deque) -> int:
    if len(history) == 1:
        return 1

    l, r, = 1, len(history) - 1
    while l <= r:
        m = (l + r) // 2
        if history[m]["date"] > date:
            l = m + 1
        elif history[m]["date"] < date:
            r = m - 1
        else:
            return m

    return l

# track stock portfolio
class Portfolio:
    def __init__(self, name: str=""):
        self.name: str = name
        self.inception: datetime = datetime.today()

        # key: ticker, value: Stock object
        self.stocks: dict[str, Stock] = {}

        self.transaction_id: int = 1
        # date: datetime, id: int, ticker: str, qty: float, price: float, fees: float
        self.history_buy: deque[dict[str, int | datetime | str | float]] = deque()
        self.history_sell: deque[dict[str,int | datetime | str | float]] = deque()

    @property
    def value_book_total(self) -> float:
        return sum(StockData.usd_to_cad(stock.value_book) if Stock.currency(stock.ticker) == "USD" else stock.value_book
                   for stock in self.stocks.values())

    @property
    def value_mkt_total(self) -> float:
        return sum(StockData.usd_to_cad(stock.value_mkt) if Stock.currency(stock.ticker) == "USD" else stock.value_mkt
                   for stock in self.stocks.values())

    @property
    def open_pl_total(self) -> float:
        return self.value_mkt_total - self.value_book_total

    @property
    def open_pl_percent_total(self) -> str:
        if self.value_book_total == 0:
            return "0.00%"
        return f"{self.open_pl_total / self.value_book_total * 100 :.2f}%"

    def get_history(self, transaction_type: str) -> []:
        transaction_type = transaction_type.lower()
        return self.history_buy if transaction_type == "buy" else self.history_sell

    def history_add(self, history_elm: {}, transaction_type: str) -> None:
        history = self.get_history(transaction_type)
        date = history_elm["date"]

        if history and date < history[0]["date"]:
            insert_index = history_insert_index(date, history)
            history.insert(insert_index, history_elm)
        else:
            history.appendleft(history_elm)

    # buying a stock
    def buy(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        # if not in portfolio, add the new stock to the portfolio
        if ticker not in self.stocks:
            stock_buying = Stock(ticker)
            self.stocks[ticker] = stock_buying
        else:
            stock_buying = self.stocks[ticker]

        # performing required calculations for buying a stock
        stock_buying.adjust_stats("buy", qty, price)

        # add to history
        history_elm = {"id": self.transaction_id, "date": date, "ticker": ticker,
                       "qty": qty, "price": price, "fee": fee}
        self.history_add(history_elm, "buy")
        self.transaction_id += 1

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
        stock_selling.adjust_stats("sell", qty, price)

        # add to history
        history_elm = {"id": self.transaction_id, "date": date, "ticker": ticker,
                       "qty": qty, "price": price, "fee": fee}
        self.history_add(history_elm, "sell")
        self.transaction_id += 1

    # return portfolio info as string
    def get_portfolio(self) -> str:
        if self.stocks:
            return "\n".join(str(stock) for stock in self.stocks.values())
        else:
            logger.warning("No portfolio")
            return "Empty portfolio"

    def remove_transaction(self):
        pass

    def str_history(self, transaction: str) -> str:
        history = self.get_history(transaction)

        if history:
            return "\n".join(
                f"id: {h['id']}, date: {h['date'].strftime('%Y-%m-%d')}, ticker: {h['ticker']}, qty: {h['qty']}, "
                f"price: {h['price']}, fee: {h['fee']}" for h in history)
        else:
            msg = f"No {transaction} history"
            logger.warning(msg)
            return msg

    def __str__(self) -> str:
        represent = f"{self.name} Portfolio Details:"
        represent += f"\n{Stock.header_str()}"
        if self.stocks:
            represent += "\n" + self.get_portfolio()
        if self.history_buy:
            represent += "\nBuy History"
            represent += "\n" + self.str_history("buy")
        if self.history_sell:
            represent += "\nSell History"
            represent += "\n" + self.str_history("sell")

        return represent

def main():
    p = Portfolio("porto")
    p.buy(Date.gen_random_day(), "GOOGL", 10, 160)
    p.buy(Date.gen_random_day(), "GOOGL", 10, 160)
    p.buy(Date.gen_random_day(), "GOOGL", 10, 160)
    p.buy(Date.gen_random_day(), "GOOGL", 10, 160)

    print(p.str_history("buy"))

if __name__ == "__main__":
    main()

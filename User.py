from datetime import datetime

from Portfolio import Portfolio
from Stock import Stock
import Date
from InvalidAction import InsufficientShares, InsufficientBalance, OverLimit
import logging
from TFSA import TFSA

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("user.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class User:
    def __init__(self, first: str, last: str, year_of_birth: int) -> None:
        self.first: str = first
        self.last: str = last
        self.year_of_birth: int = year_of_birth
        self.tfsa = TFSA(year_of_birth)
        self.portfolio = Portfolio()

        # track stock portfolio
        # self.portfolio: dict[str, Stock] = {}
        # date: datetime, type ("buy"/"sell"): str, ticker: str, qty: float, price: float, fees: float
        self.history_buy: list[tuple[datetime, str, str, float, float, float]] = []
        self.history_sell: list[tuple[datetime, str, str, float, float, float]] = []

        logger.info(f"Created User: {self.first} {self.last} {self.year_of_birth}")

    @property
    def name_fl(self) -> str:
        return f"{self.first} {self.last}"

    @property
    def name_lf(self) -> str:
        return f"{self.last}, {self.first}"


    # buying a stock
    # precondition: must have sufficient cash balance
    def buy(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        logger.info(f"Buying {ticker}")

        # check if balance is sufficient to process purchase
        remain = self.tfsa.balance - (qty * price) - fee
        if remain < 0:
            raise InsufficientBalance(f"Cannot buy {ticker} as doing so would put account balance at -${-remain:.2f}.")

        self.tfsa.balance = remain # subtract balance based on how much bought

        self.portfolio.buy(date, ticker, qty, price, fee)


    # selling a stock
    # precondition: must own sufficient shares to sell
    def sell(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        logger.info(f"Selling {ticker}")

        try:
            self.portfolio.sell(date, ticker, qty, price, fee)
        except InsufficientShares as e:
            logger.exception(e)
        else: # if no exception caught
            self.tfsa.balance -= fee # subtract fee from balance
            self.tfsa.balance += (qty * price) # add balance based on how much sold



    # str of user object
    def __str__(self) -> str:
        represent = f"Details for {self.name_lf}:"
        my_tfsa = self.tfsa

        # basic tfsa account details
        represent += (f"\nTotal Limit: ${my_tfsa.limit_total:,.2f}, Avl Limit: ${my_tfsa.limit_avl:,.2f}, "
                      f"Balance: ${my_tfsa.balance:,.2f}, Avl Room: ${my_tfsa.room_avl:,.2f}")

        # list of all contributions
        if my_tfsa.contributions:
            represent += "\nContributions:\n"
            represent += "\n".join(f"Date: {c[0]}, Amount: ${c[1]:,.2f}" for c in my_tfsa.contributions)

        # list of all withdrawals
        if my_tfsa.withdrawals:
            represent += "\nWithdrawals:\n"
            represent += "\n".join(f"Date: {w[0]}, Amount: ${w[1]:,.2f}" for w in my_tfsa.withdrawals)

        # list of all owned stocks
        if self.portfolio:
            represent += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPortfolio:"
            represent += f"\n{Stock.header_str()}\n"
            represent += self.portfolio.get_portfolio()

        return represent

def main():
    logger.info("\n\n\nBeginning log\n\n")
    joe_biden = User("Joe", "Biden", 2002)

    try:
        joe_biden.tfsa.contribute(Date.gen_random_day(), 15000)
        joe_biden.tfsa.contribute(Date.gen_random_day(), 10000)
        # joe_biden.contribute(SelectDate.gen_random_day(), 10000)
        # print("contributed 3 times")
    except OverLimit as e:
        logger.exception(e)

    try:
        joe_biden.tfsa.withdraw(Date.gen_random_day(), 10000)
        joe_biden.tfsa.withdraw(Date.gen_random_day(), 10000)
        # joe_biden.withdraw(SelectDate.gen_random_day(), 120000)
        # print("withdrew 3 times")
    except InsufficientBalance as e:
        logger.exception(e)

    try:
        ticker = "gooGl".upper()
        joe_biden.buy(Date.gen_random_day(), ticker, 10, 160)
        joe_biden.buy(Date.gen_random_day(), "GOOGL", 20, 100)
        ticker = "AapL".upper()
        joe_biden.buy(Date.gen_random_day(), ticker, 5, 100)
        # joe_biden.buy(SelectDate.gen_random_day(), "AAPL", 5, 100)
    except InsufficientBalance as e:
        logger.exception(e)

    # try:
    #     joe_biden.sell("GOOGL", 32, 120)
    # except InsufficientShares as e:
    #     logger.exception(e)

    print(f"\n{Stock.header_str()}")
    print(joe_biden.portfolio.get_portfolio())

    # try:
    joe_biden.sell(Date.gen_random_day(), "GOOGL", 5, 160)
    joe_biden.sell(Date.gen_random_day(), "GOOGL", 5, 200)

    #     joe_biden.sell("TSLA", 10, 10)
    # except InsufficientShares as e:
    #     logger.exception(e)

    print()

    joe_biden.buy(Date.gen_random_day(), "TEST", 4, 80)
    joe_biden.sell(Date.gen_random_day(), "TEST", 4, 60)
    # joe_biden.buy(SelectDate.gen_random_day(), "AMZN", 4, 100)
    print(joe_biden.portfolio.stocks["GOOGL"].value_book_sell)
    print(joe_biden)
    print(joe_biden.portfolio.get_history_buy())
    print(joe_biden.portfolio.get_history_sell())

if __name__ == "__main__":
    main()

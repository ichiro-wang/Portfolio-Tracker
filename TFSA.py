import logging
from datetime import datetime
import Date
from InvalidAction import OverLimit, InsufficientBalance
from Portfolio import Portfolio
from Portfolio import history_insert_index # helper method to keep history sorted
from collections import deque

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("logs/tfsa.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

TFSA_LIMIT = {2009: 5000, 2010: 5000, 2011: 5000, 2012: 5000, 2013: 5500, 2014: 5500, 2015: 10000, 2016: 5500,
              2017: 5500, 2018: 5500, 2019: 6000, 2020: 6000, 2021: 6000, 2022: 6000, 2023: 6500, 2024: 7000}

class TFSA:
    def __init__(self, year_of_birth: int):
        self.year_eligible = max(year_of_birth + 18, 2009) # tfsa room builds up starting at 18
        self.balance_cash: float = 0 # represents cash balance_cash

        self.transaction_id = 0
        # tracking contribution and withdrawal history as list of dicts
        self.contributions: deque[dict[str, datetime | float]] = deque()
        self.withdrawals: deque[dict[str, datetime | float]] = deque()

        self.portfolio: Portfolio = Portfolio()

    # how much tfsa space the user should have based on CRA limits
    @property
    def limit_total(self) -> float:
        if self.year_eligible > 2024:
            return 0

        # add limit of each year when eligible
        return sum(TFSA_LIMIT[year] for year in TFSA_LIMIT if year >= self.year_eligible)

    # available limit changes based on when withdrawal was made
    # withdrawal is not realized until the year passes
    @property
    def limit_avl(self) -> float:
        unrealized_w = sum(w["amount"] for w in self.withdrawals if Date.this_year(w["date"]))

        return self.limit_total - unrealized_w

    # available contribution room based on realized withdrawals
    @property
    def room_avl(self) -> float:
        return self.limit_avl - self.balance_cash

    def get_cont_room_by_year(self) -> dict[int, int]:
        return {year: TFSA_LIMIT[year] for year in TFSA_LIMIT if self.year_eligible <= year}

    def history_add(self, history_elm: {}, transaction_type: str) -> None:
        transaction_type = transaction_type.lower()
        history = self.contributions if transaction_type == "contribution" else self.withdrawals
        date = history_elm["date"]

        if history and date < history[0]["date"]:
            insert_index = history_insert_index(date, history)
            history.insert(insert_index, history_elm)
        else:
            history.appendleft(history_elm)

    # contributing to tfsa
    # precondition: added amount must not go over available limit
    def contribute(self, date: datetime, amount: float) -> None:
        logger.info(f"Contributing: ${amount:,.2f}")
        balance_new = self.balance_cash + amount

        if balance_new > self.limit_avl:
            raise OverLimit(f"Cannot contribute. Current available TFSA limit is ${self.limit_avl:.2f}. "
                            f"Contributing ${amount:.2f} would put TFSA at ${balance_new:.2f}. "
                            f"Transaction not accepted.")

        self.balance_cash = balance_new

        # add to history
        history_elm = {"id": self.transaction_id, "date": date, "amount": amount}
        self.history_add(history_elm, "contribution")
        self.transaction_id += 1

    # withdrawing from tfsa
    # precondition: account must have sufficient cash balance_cash to withdraw
    def withdraw(self, date: datetime, amount: float) -> None:
        logger.info(f"Withdrawing: ${amount:,.2f}")
        remain = self.balance_cash - amount
        if remain < 0:
            raise InsufficientBalance(
                f"Cannot withdraw. Withdrawal would put account balance at: -${-remain:.2f}. Transaction not accepted.")

        self.balance_cash = remain

        history_elm = {"id": self.transaction_id, "date": date, "amount": amount}
        self.history_add(history_elm, "withdrawal")
        self.transaction_id += 1


    """
    # buying a stock
    # precondition: must have sufficient cash balance_cash
    def buy(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        logger.info(f"Buying {ticker}")

        # check if balance_cash is sufficient to process transaction
        transaction = qty * price + fee
        if Stock.currency(ticker) == "USD":
            transaction = usd_to_cad(transaction)

        remain = self.balance_cash - transaction
        if remain < 0:
            raise InsufficientBalance(f"Cannot buy {ticker} as doing so would put account balance at -${-remain:.2f}.")

        self.balance_cash = remain # subtract balance_cash based on how much bought
        self.portfolio.buy(date, ticker, qty, price, fee)

    # selling a stock
    # precondition: must own sufficient shares to sell
    def sell(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        logger.info(f"Selling {ticker}")

        try:
            self.portfolio.sell(date, ticker, qty, price, fee)
        except InsufficientShares as e:
            logger.exception(e)
        else:
            # gain: qty * price, loss: fee
            transaction = qty * price - fee
            if Stock.currency(ticker) == "USD":
                transaction = usd_to_cad(transaction)

            self.balance_cash += transaction
    """

    def str_history(self, transaction_type: str) -> str:
        history = self.contributions if transaction_type == "contribution" else self.withdrawals

        if history:
            return "\n".join(f"ID: {h['id']} {h['date']:}, Date: {h['date']:}, Amount: ${h['amount']:,.2f}"
                             for h in history)
        return ""

    def __str__(self):
        # basic tfsa account details
        represent = "TFSA Account Details:"
        represent += (f"\nTotal Limit: ${self.limit_total:,.2f}, Avl Limit: ${self.limit_avl:,.2f}, "
                      f"Balance: ${self.balance_cash:,.2f}, Avl Room: ${self.room_avl:,.2f}")
        # list of all contributions
        if self.contributions:
            represent += "\nContributions:\n"
            represent += self.str_history("contribution")
        # list of all withdrawals
        if self.withdrawals:
            represent += "\nWithdrawals:\n"
            represent += self.str_history("withdrawal")

        return represent

def main():
    acc = TFSA(2002)

    try:
        acc.contribute(Date.select_date(), 3000)
        acc.contribute(Date.select_date(), 3000)
        acc.contribute(Date.select_date(), 3000)
        acc.contribute(Date.select_date(), 3000)
        acc.contribute(Date.select_date(), 30000)
    except OverLimit as e:
        logger.exception(e)

    try:
        acc.withdraw(Date.select_date(), 2000)
        acc.withdraw(Date.select_date(), 2000)
        acc.withdraw(Date.select_date(), 2000)
        acc.withdraw(Date.select_date(), 2000)
        acc.withdraw(Date.select_date(), 20000)
    except InsufficientBalance as e:
        logger.exception(e)

    print(acc)
    print(acc.get_cont_room_by_year())


if __name__ == '__main__':
    main()
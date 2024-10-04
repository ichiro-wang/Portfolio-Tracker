import logging
from datetime import datetime
import Date
from InvalidAction import OverLimit, InsufficientBalance, InsufficientShares
from Portfolio import Portfolio

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("tfsa.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

TFSA_LIMIT = {2009: 5000, 2010: 5000, 2011: 5000, 2012: 5000, 2013: 5500, 2014: 5500, 2015: 10000, 2016: 5500,
              2017: 5500, 2018: 5500, 2019: 6000, 2020: 6000, 2021: 6000, 2022: 6000, 2023: 6500, 2024: 7000}


class TFSA:
    def __init__(self, year_of_birth: int):
        self.year_eligible = max(year_of_birth + 18, 2009) # eligibility starts at 18
        self.balance: float = 0 # represents cash balance

        # tracking contribution snd withdrawal history as list of [(date, amount)]
        self.contributions: list[tuple[datetime, float]] = []
        self.withdrawals: list[tuple[datetime, float]] = []

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
        unrealized_w = sum(w[1] for w in self.withdrawals if Date.this_year(w[0]))

        return self.limit_total - unrealized_w

    # available contribution room based on realized withdrawals
    @property
    def room_avl(self) -> float:
        return self.limit_avl - self.balance

    # contributing to tfsa
    # precondition: added amount must not go over available limit
    def contribute(self, date: datetime, amount: float) -> None:
        logger.info(f"Contributing: ${amount:,.2f}")
        balance_new = self.balance + amount

        if balance_new > self.limit_avl:
            raise OverLimit(f"Cannot contribute. Current available TFSA limit is ${self.limit_avl:.2f}. "
                            f"Contributing ${amount:.2f} would put TFSA at ${balance_new:.2f}. "
                            f"Transaction not accepted.")

        self.balance = balance_new
        self.contributions.append((date, amount))

    # withdrawing from tfsa
    # precondition: account must have sufficient cash balance to withdraw
    def withdraw(self, date: datetime, amount: float) -> None:
        logger.info(f"Withdrawing: ${amount:,.2f}")
        remain = self.balance - amount
        if remain < 0:
            raise InsufficientBalance(
                f"Cannot withdraw. Withdrawal would put account balance at: -${-remain:.2f}. Transaction not accepted.")

        self.balance = remain
        self.withdrawals.append((date, amount))


    # buying a stock
    # precondition: must have sufficient cash balance
    def buy(self, date: datetime, ticker: str, qty: float, price: float, fee: float=0) -> None:
        logger.info(f"Buying {ticker}")

        # check if balance is sufficient to process purchase
        remain = self.balance - (qty * price) - fee
        if remain < 0:
            raise InsufficientBalance(f"Cannot buy {ticker} as doing so would put account balance at -${-remain:.2f}.")

        self.balance = remain # subtract balance based on how much bought

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
            self.balance -= fee # subtract fee from balance
            self.balance += (qty * price) # add balance based on how much sold

    def __str__(self):
        # basic tfsa account details
        represent = (f"\nTotal Limit: ${self.limit_total:,.2f}, Avl Limit: ${self.limit_avl:,.2f}, "
                      f"Balance: ${self.balance:,.2f}, Avl Room: ${self.room_avl:,.2f}")
        # list of all contributions
        if self.contributions:
            represent += "\nContributions:\n"
            represent += "\n".join(f"Date: {c[0]:}, Amount: ${c[1]:,.2f}" for c in self.contributions)
        # list of all withdrawals
        if self.withdrawals:
            represent += "\nWithdrawals:\n"
            represent += "\n".join(f"Date: {w[0]}, Amount: ${w[1]:,.2f}" for w in self.withdrawals)

        return represent

def main():
    acc = TFSA(2000)
    print(acc)

if __name__ == '__main__':
    main()
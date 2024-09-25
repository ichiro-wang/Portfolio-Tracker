from Stock import Stock
from SelectDate import select_date, this_year
from InvalidAction import InsufficientShares, InsufficientBalance, OverLimit

TFSA_LIMIT = {2009: 5000, 2010: 5000, 2011: 5000, 2012: 5000, 2013: 5500, 2014: 5500, 2015: 10000, 2016: 5500,
              2017: 5500, 2018: 5500, 2019: 6000, 2020: 6000, 2021: 6000, 2022: 6000, 2023: 6500, 2024: 7000}


class User:
    def __init__(self, first, last, yob) -> None:
        self.first = first
        self.last = last
        self.yob = yob # year of birth for calculating tfsa limit

        self.balance = 0 # represents cash balance

        self.contributions = []
        self.withdrawals = []

        self.limit_total = self.limit_total_calc()
        # self.limit_avl = self.limit_total

        self.portfolio = {}

    @property
    def name_fl(self) -> str:
        return f"{self.first} {self.last}"

    @property
    def name_lf(self) -> str:
        return f"{self.last}, {self.first}"

    @property
    def limit_avl(self) -> int:
        unrealized_w = 0
        for w in self.withdrawals:
            if this_year(w[0]):
                unrealized_w += w[1]
        return self.limit_total - unrealized_w

    def limit_total_calc(self) -> int:
        # tfsa started in 2009
        # contribution starts when one turns 18 (assuming canadian citizen)
        year_start = max(self.yob + 18, 2009)
        if year_start > 2024:
            return 0

        limit_total = sum(TFSA_LIMIT[year] for year in TFSA_LIMIT if year >= year_start)

        return limit_total

    @property
    def room_avl(self) -> int:
        return self.limit_avl - self.balance

    def contribute(self, amount) -> None:
        print(f"Contributing: ${amount:,.2f}")
        balance_new = self.balance + amount

        if balance_new > self.limit_avl:
            raise OverLimit(f"Cannot contribute. Current available TFSA limit is ${self.limit_avl:.2f}. "
                            f"Contributing ${amount:.2f} would put TFSA at ${balance_new:.2f}. "
                            f"Transaction not accepted.")

        self.balance = balance_new
        self.contributions.append((select_date(), amount))

    def withdraw(self, amount) -> None:
        print(f"Withdrawing: ${amount:,.2f}")
        remain = self.balance - amount

        if remain < 0:
            raise InsufficientBalance(
                f"Cannot withdraw. Withdrawal would put account balance at: -${-remain:.2f}. Transaction not accepted.")

        self.balance = remain
        self.withdrawals.append((select_date(), amount))

    # buying a stock
    # precondition: must have sufficient balance (cash)
    def buy(self, ticker, qty, price):
        # if not in portfolio, add the new stock to the portfolio
        if ticker not in self.portfolio:
            new_stock = Stock(ticker)
            self.portfolio[ticker] = new_stock

        # check if balance is sufficient to process purchase
        remain = self.balance - (qty * price)
        if remain < 0:
            raise InsufficientBalance(f"Cannot buy {ticker} as doing so would put account balance at -${-remain:.2f}.")

        # call buy method from stock object
        self.portfolio[ticker].buy(qty, price)
        self.balance = remain

    # selling a stock
    # precondition: must own sufficient shares to sell
    def sell(self, ticker, qty, price):

        if ticker not in self.portfolio:
            raise InsufficientShares(f"Cannot sell {ticker} as you do not own any shares. Transaction not accepted.")

        self.portfolio[ticker].sell(qty, price)
        self.balance += (qty * price)

    # printing user object
    def __str__(self) -> str:
        represent = f"Details for {self.name_lf}:"

        represent += (f"\nTotal Limit: ${self.limit_total:,.2f}, Avl Limit: ${self.limit_avl:,.2f}, "
                      f"Balance: ${self.balance:,.2f}, Avl Room: ${self.room_avl:,.2f}")

        if self.contributions:
            represent += "\nContributions:"
            for c in self.contributions:
                represent += f"\nDate: {c[0]}, Amount: ${c[1]:,.2f}"
        if self.withdrawals:
            represent += "\nWithdrawals:"
            for w in self.withdrawals:
                represent += f"\nDate: {w[0]}, Amount: ${w[1]:,.2f}"

        if self.portfolio:
            represent += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPortfolio:"
            for s in self.portfolio:
                represent += f"\n{self.portfolio[s]}"

        return represent


def main():
    joe_biden = User("Joe", "Biden", 2002)

    print(joe_biden.limit_avl)

    try:
        joe_biden.contribute(15000)
        joe_biden.contribute(10000)
        joe_biden.contribute(10000)
        print("contributed 3 times")
    except OverLimit as e:
        print(e)

    try:
        joe_biden.withdraw(10000)
        joe_biden.withdraw(10000)
        joe_biden.withdraw(120000)
        print("withdrew 3 times")
    except InsufficientBalance as e:
        print(e)

    try:
        ticker = "GOOGL"
        joe_biden.buy(ticker, 10, 160)
        joe_biden.buy("GOOGL", 20, 100)
        ticker = "AAPL"
        joe_biden.buy(ticker, 5, 300)
        joe_biden.buy("AAPL", 5, 300)
    except InsufficientBalance as e:
        print(e)

    try:
        joe_biden.sell("GOOGL", 32, 120)
    except InsufficientShares as e:
        print(e)

    # print()
    # print(joe_biden)


if __name__ == "__main__":
    main()

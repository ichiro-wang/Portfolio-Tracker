from StockData import get_price
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("stock.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Stock:

    def __init__(self, ticker: str, comment="") -> None:
        self.ticker = ticker.upper()  # ticker symbol
        self.comment = comment  # empty by default
        self.qty_open = 0  # how many shares currently owned
        self.qty_closed = 0  # how many shares sold
        self.value_book = 0  # how much the shares were bought for (sum)

        # how many have i bought historically, how much as that costed, and the avg price of the stock when i bought
        self.qty_total = 0  # how many shares bought in total
        self.value_total = 0  # how much spent buying total shares
        self.price_avg = 0  # avg stock price when bought shares

        # transaction history
        self.history_buy = []  # track history of buys
        self.history_sell = []  # track history of sells


    # buying a stock
    # def buy(self, qty: float, price: float) -> None:
    #     print(f"Recording new buy for {self.ticker}")
    #     self.qty_open += qty
    #     self.value_book += (qty * price)
    #
    #     self.qty_total += qty
    #     self.value_total += (qty * price)
    #     self.price_avg = self.value_total / self.qty_total
    #
    #     # save to history with date
    #     self.history_buy.append((select_date(), qty, price))

    # selling a stock
    # precondition: must have sufficient shares
    # def sell(self, qty: float, price: float) -> None:
    #     print(f"Recording new sell for {self.ticker}")
    #     qty_remain = self.qty_open - qty
    #     if qty_remain < 0:
    #         raise InsufficientShares(f"Selling {qty} shares will leave a negative quantity. Transaction not accepted.")
    #
    #     self.qty_open = qty_remain
    #     self.qty_closed += qty
    #
    #     self.value_book -= (qty * price)
    #
    #     # save to history with date
    #     self.history_sell.append((select_date(), qty, price))

    @staticmethod
    def header_str():
        print(f'{"Ticker":.<8}{"Open Qty":.<10}{"Closed Qty":.<12}{"Avg Price":.<14}{"Mkt Price":.<14}'
              f'{"Book Value":.<16}{"Mkt Value":.<15}{"Open P&L":.<14}{"% Open P&L":.<14}')

    def __str__(self) -> str:
        # price = get_price(self.ticker)
        price = get_price(self.ticker)
        value_mkt = price * self.qty_open
        pl = value_mkt - self.value_book
        # print(self.qty_open, self.qty_total, self.value_total, self.price_avg)
        ppl = f"{pl / self.value_book * 100 :,.2f}%"
        string = (f"{self.ticker:<8}{self.qty_open:<10}{self.qty_closed:<12}${self.price_avg:<13,.1f}${price:<13,.2f}"
                  f"${self.value_book:<15,.2f}${value_mkt:<14,.2f}${pl:<13,.2f}{ppl:<14}")

        return string


    # repr of stock object
    def __repr__(self) -> str:
        represent = (f"Details for {self.ticker}:\nOpen Qty: {self.qty_open}, Avg Price: ${self.price_avg:,.2f}, " +
                     (f"Book Value: ${self.value_book:,.2f}" if self.value_book >= 0
                      else f"Book Value: -${-self.value_book:,.2f}"))
        if self.history_buy:
            represent += "\nBuy History:"
            for buy in self.history_buy:
                represent += f"\nDate: {buy[0].strftime('%x')}, Qty: {buy[1]}, Price: ${buy[2]:,.2f}"
        if self.history_sell:
            represent += "\nSell History:"
            for sell in self.history_sell:
                represent += f"\nDate: {sell[0].strftime('%x')}, Qty: {sell[1]}, Price: ${sell[2]:,.2f}"
        represent += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        return represent


def main():
    stock = Stock("TSLA", "elon musk")

    # stock.buy(2, 200)
    # stock.buy(2, 200)
    #
    # stock.sell(2, 250)

    # stock.buy(10, 100)
    # stock.buy(20, 200)
    # stock.buy(15, 50)
    #
    # try:
    #     stock.sell(5, 300)
    #     stock.sell(10, 60)
    #     stock.sell(35, 60)
    # except InsufficientShares as e:
    #     print(e)
    # finally:
    #     print(stock)
    # print(repr(stock))

    Stock.header_str()
    # print(stock)


if __name__ == "__main__":
    main()
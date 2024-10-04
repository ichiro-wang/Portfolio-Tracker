from datetime import datetime, timedelta
from random import randrange
from InvalidAction import InvalidDate
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - '
                                  '%(module)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("date.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def select_date() -> datetime:
    # while True:
    #     date_entry = input("Enter date of transaction in yyyy-mm-dd format (or 'today'): ")
    #
    #     if date_entry == "today":
    #         return datetime.today()
    #
    #     try:
    #         year, month, day = map(int, date_entry.split("-"))
    #         date_obj = datetime(year, month, day)
    #         valid_date(date_obj)
    #     except InvalidDate as e:
    #         print(e)
    #     except ValueError:
    #         print("Please enter a valid date using proper format with dashes.")
    #     else:
    #         return date_obj #.strftime('%Y-%m-%d')

    return gen_random_day()

# check if given date is valid
def valid_date(date: datetime) -> None:
    if date >= datetime.today():
        raise InvalidDate("Cannot process transactions that occur in the future.")
    if date <= datetime.today() - timedelta(days=365*20):
        raise InvalidDate("Cannot process transactions that occur over 20 years ago.")

# check if a given date falls on this year
def this_year(date: datetime) -> bool:
    if date.year == datetime.today().year:
        return True
    return False

# a random day generator to automate date selection
# only used for testing
def gen_random_day() -> datetime:
    logger.info("Creating random date")

    start = datetime(2020, 1, 1)
    end = datetime.today()
    delta = end - start
    random_day = randrange(delta.days)

    return start + timedelta(random_day) #.strftime('%Y-%m-%d')

def main():
    a_day = select_date()
    print(a_day)

if __name__ == "__main__":
    main()
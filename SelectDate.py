from datetime import datetime, timedelta
from random import randrange
from InvalidAction import InvalidDate
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("date.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def select_date():
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
    #     except ValueError as e:
    #         print("Please enter a valid date using proper format with dashes.")
    #     else:
    #         return date_obj


    return gen_random_day()

# check if
def valid_date(a_date: datetime):
    if a_date >= datetime.today():
        logging.warning("Invalid date: Future")
        raise InvalidDate("Cannot process transactions that occur in the future.")
    if a_date <= datetime.today() - timedelta(days=365*20):
        logging.warning("Invalid date: Too far in past")
        raise InvalidDate("Cannot process transactions that occur over 20 years ago.")

# check if a given date falls on this year
def this_year(a_date: datetime):
    if a_date.year == datetime.today().year:
        return True
    logging.warning("Date does not fall on this year")
    return False

# a random day generator to automate date selection
# only used for testing
def gen_random_day():

    logging.info("Creating random date")

    start = datetime(2020, 1, 1)
    end = datetime.today()
    delta = end - start
    random_day = randrange(delta.days)

    return start + timedelta(random_day)

def main():
    a_day = select_date()
    print(a_day)

if __name__ == "__main__":
    main()
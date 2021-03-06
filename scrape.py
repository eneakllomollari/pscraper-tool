import datetime
import logging
import time

import schedule
from pscraper.scraper.marketplaces import scrape_autotrader, scrape_cars
from pscraper.utils.misc import send_slack_message, send_slack_report

logging.basicConfig(filename=f'logs/{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}.log',
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', level=logging.NOTSET)


def main_job():
    try:
        cars = scrape_cars()
        autotrader = scrape_autotrader()
        send_slack_report(cars, autotrader, 'All States')
    except (ValueError, IndexError, AssertionError):
        send_slack_message()


if __name__ == '__main__':
    schedule.every().day.at('07:00').do(main_job)  # 07:00 is midnight
    while True:
        schedule.run_pending()
        time.sleep(60)

#! venv3/bin/python
import datetime
import logging
import time

import schedule
from pscraper.scraper import pscrape
from pscraper.utils.misc import send_slack_message, send_slack_report

logging.basicConfig(filename=f'logs/{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}.log',
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', level=logging.NOTSET)


def main_job():
    try:
        cars, autotrader = pscrape()
        send_slack_report([0, cars], [0, autotrader], 'All States', channel='#daily-job')
    except (ValueError, IndexError, AssertionError):
        send_slack_message()


if __name__ == '__main__':
    # 07:00 is midnight
    schedule.every().day.at('07:00').do(main_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

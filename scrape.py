#! venv3/bin/python
import logging
import time
from getpass import getuser
from multiprocessing import Process, Queue
from os import getenv

import schedule
from pscraper.api import API
from pscraper.scraper.marketplaces import scrape
from pscraper.scraper.marketplaces.consts import CURR_DATE
from pscraper.utils.misc import get_traceback, send_slack_message, send_slack_report
from yaml import safe_load

logger = logging.getLogger(__name__)


def scrape_job(zip_code, search_radius, target_states, return_queue):
    api = API('phevscraping', getenv('PSCRAPER_PASSWORD'), localhost=True if getuser() == 'enea' else False)
    try:
        cars, autotrader, carmax = scrape(zip_code, search_radius, target_states, api)
        return_queue.put([cars, autotrader, carmax, target_states])
    except (ValueError, IndexError, AssertionError):
        logger.critical('Error in scrape_job!', exc_info=get_traceback())
        send_slack_message(channel='#daily-job')


def build_and_post_report(ret_queue):
    states = []
    cars_et, cars_count, at_et, at_count, carmax_et, carmax_count = 0, 0, 0, 0, 0, 0
    while not ret_queue.empty():
        items = ret_queue.get()
        cars, autotrader, carmax = items[0], items[1], items[2]
        states.extend(items[3])

        cars_et += cars[0]
        cars_count += cars[1]
        at_et += autotrader[0]
        at_count += autotrader[1]
        carmax_et += carmax[0]
        carmax_count += carmax[1]

    states = ', '.join(set(states))
    cars_et, at_et, carmax_et = round(cars_et, 2), round(at_et, 2), round(carmax_et, 2)
    send_slack_report(cars_et, cars_count, at_et, at_count, carmax_et, carmax_count, states)


def main_job():
    logging.basicConfig(filename=f'logs/{CURR_DATE}.log', level=logging.NOTSET,
                        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    with open('config.yml') as fd:
        run_config = safe_load(fd)
    return_queue = Queue()
    processes = [Process(target=scrape_job, args=(*config, return_queue)) for config in run_config.values()]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    build_and_post_report(return_queue)


if __name__ == '__main__':
    # 07:00 is midnight
    schedule.every().day.at('07:00').do(main_job)

    while True:
        schedule.run_pending()
        time.sleep(60)

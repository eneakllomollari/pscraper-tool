from pscraper import scrape
from pscraper.utils.helpers import update_duration_and_history, load_yaml_file
from pscraper.utils.io import get_master_table, save_master_table
from pscraper.utils.map import build_map
from pscraper.utils.notifications import notify
from pscraper.utils.summary import summarize

from config_keys import SEARCH_RADIUS, ZIP_CODE, TARGET_STATES, PRICE_HISTORY, DEALERSHIP_HISTORY, \
    MASTER_TABLE, DEALER_MAP, DEALER_GEOLOCATION, SUMMARY_ALL, SUMMARY_SOLD


def main(config):
    master_table = get_master_table(config[MASTER_TABLE])
    vehicle_list = scrape(config[ZIP_CODE], config[SEARCH_RADIUS], config[TARGET_STATES])
    for vehicle in vehicle_list:
        master_table[vehicle.listing_id] = update_duration_and_history(
            price_history=config[PRICE_HISTORY],
            seller_history=config[DEALERSHIP_HISTORY],
            vehicle=vehicle,
            mastertable=master_table)
    save_master_table(master_table, config[MASTER_TABLE])


if __name__ == '__main__':
    configuration = load_yaml_file('config.yml')
    # noinspection PyBroadException
    try:
        main(configuration)
        summarize(configuration[MASTER_TABLE], configuration[SUMMARY_ALL], configuration[SUMMARY_SOLD])
        build_map(
            mastertable_path=configuration[MASTER_TABLE],
            dealers_geoloc=configuration[DEALER_GEOLOCATION],
            dealer_map_loc=configuration[DEALER_MAP],
        )
        notify(configuration)
    except Exception as e:
        notify(configuration, is_failure=True)

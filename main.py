from pscraper.scraper import scrape
from pscraper.utils import send_slack_message

zip_code, search_radius, target_states = '95616', '30', ['CA']

if __name__ == '__main__':
    try:
        scrape_report = scrape(zip_code, search_radius, target_states)
        send_slack_message('#daily-job', scrape_report)
    except (ValueError, IndexError) as e:
        send_slack_message('#daily-job')

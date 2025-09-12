import time
import logging
import sys

from requests.exceptions import HTTPError
import schedule

from strava_stats.strava_api import save_strava_activities


logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stdout, level=logging.INFO)

def sync_strava_activities():
    logging.info("syncing strava activities")
    try:
        save_strava_activities("strava_stats/data/activities.json")
    except HTTPError:
        logging.error("error syncing strava activities")


# Run initially
sync_strava_activities()

# And then every 3 hours
schedule.every(3).hours.do(sync_strava_activities)
while True:
    schedule.run_pending()
    time.sleep(1)

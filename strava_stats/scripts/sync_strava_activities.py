import time
import logging
import sys

import schedule

from strava_stats.strava_api import save_strava_activities


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def sync_strava_activities():
    logging.info("syncing strava activities")
    save_strava_activities("strava_stats/data/activities.json")


# Run initially
sync_strava_activities()

# And then every hour
schedule.every().hour.do(sync_strava_activities)
while True:
    schedule.run_pending()
    time.sleep(1)

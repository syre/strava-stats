import time
import logging

import schedule

from strava_stats.strava_api import save_strava_activities

def strava_sync():
    logging.info("syncing strava activities")
    save_strava_activities("../data/activities.json")


#schedule.every().hour.do(strava_sync)
schedule.every(3).minutes.do(strava_sync)
schedule.run_all()
#while True:
#    schedule.run_pending()
#    time.sleep(1)

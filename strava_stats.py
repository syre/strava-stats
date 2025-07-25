import json
import datetime
from collections import defaultdict

import numpy as np
import pandas as pd

from strava_api import get_activities, get_access_token

def save_strava_activities(path='activities.json'):
    """ Save Strava activities to a JSON file."""
    access_token = get_access_token()
    activities_list = []
    utc_today = datetime.datetime.now(datetime.UTC)
    earliest_date_found = utc_today.strftime("%Y-%m-%dT%H:%M:%SZ")

    # iterates over pages until we get the earliest date found
    # TODO: probably there is a better iteration strategy
    for i in range(1, 999):
        activities = get_activities(access_token, page=i)
        if not activities:
            break
        if earliest_date_found == activities[-1]["start_date"]:
            break
        earliest_date_found = activities[-1]["start_date"]
        activities_list += activities

    json.dump(activities_list, open(path, 'w'))

def load_strava_activities(path='activities.json') -> dict:
    """Loads saved Strava activities from a JSON file."""
    activities = json.load(open(path, 'r'))
    if not activities:
        raise ValueError("No activities found in the JSON file.")
    return activities

def generate_km_per_day_over_year_heatmap_data(activities: list[dict], year=None):
    """Generates heatmap data for kilometers per day over year."""
    if not year:
        year = datetime.datetime.now().year

    heatmap_arr = np.zeros((12, 31))
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_year = int(date.split("-")[0])
        if parsed_year != year:
            continue
        parsed_distance = activity["distance"] / 1000
        parsed_month = int(date.split("-")[1]) - 1
        parsed_day = int(date.split("-")[2])

        heatmap_arr[parsed_month, parsed_day - 1] += parsed_distance
    return heatmap_arr


def generate_distance_for_year(activities: list[dict], year=None):
    """Generates total kilometers for a given year."""
    if not year:
        year = datetime.datetime.now().year

    distance_sum = 0
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_year = int(date.split("-")[0])
        if parsed_year != year:
            continue
        parsed_distance = activity["distance"] / 1000
        distance_sum += parsed_distance
    return distance_sum

def generate_streak_for_year(activities: list[dict], from_date=None):
    """Generates the streak of consecutive days with activities from a given date."""
    if not from_date:
        from_date = datetime.datetime.now().date()

    streak = 0
    parsed_dates_dict = defaultdict(bool)

    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if parsed_date > from_date:
            break
        parsed_dates_dict[date] = True

    while True:
        if parsed_dates_dict[from_date.strftime("%Y-%m-%d")]:
            streak += 1
        else:
            break
        from_date -= datetime.timedelta(days=1)
    return streak

def generate_num_rides_for_year(activities: list[dict], year=None):
    """Generates the number of rides for a given year."""
    if not year:
        year = datetime.datetime.now().year

    num_rides = 0
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_year = int(date.split("-")[0])
        if parsed_year != year:
            continue
        num_rides += 1
    return num_rides

def generate_moving_time_for_year(activities: list[dict], year=None):
    """Generates the moving time for a given year."""
    if not year:
        year = datetime.datetime.now().year

    moving_time = 0
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_year = int(date.split("-")[0])
        if parsed_year != year:
            continue
        parsed_moving_time = activity["moving_time"]
        moving_time += parsed_moving_time
    return moving_time

def generate_ride_length_binned_over_year_data(activities: list[dict], year=None):
    """Generates binned ride length counts over a given year for bar plotting."""
    if not year:
        year = datetime.datetime.now().year

    # Extract distances in km for the specified year
    distance_list = []
    for activity in activities:
        date_str = activity["start_date"].split("T")[0]
        parsed_year = int(date_str.split("-")[0])
        if parsed_year != year:
            continue
        distance_km = activity["distance"] / 1000
        distance_list.append(distance_km)

    # Create bins: 0-10, 10-20, ..., 90-100, 100+
    bins_edges = list(range(0, 101, 10)) + [float('inf')]
    bin_labels = [f"{i}-{i+10}" for i in range(0, 100, 10)] + ["100+"]

    if not distance_list:
        return pd.DataFrame({'Distance Bin': bin_labels, 'Count': [0]*len(bin_labels)})

    binned = pd.cut(distance_list, bins=bins_edges, labels=bin_labels, right=False, include_lowest=True)
    counts = binned.value_counts().sort_index()

    df = pd.DataFrame({
        "Distance Bin": counts.index,
        "Count": counts.values
    })

    return df


if __name__ == '__main__':
    save_strava_activities()

import json
import datetime
from collections import defaultdict
from typing import Optional

import numpy as np
import pandas as pd

from strava_api import get_activities, get_access_token

def save_strava_activities(path: str = 'activities.json'):
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

def load_strava_activities(path='activities.json') -> list[dict]:
    """Loads saved Strava activities from a JSON file."""
    activities = json.load(open(path, 'r'))
    if not activities:
        raise ValueError("No activities found in the JSON file.")
    return activities

def filter_strava_activities_by_year(activities: list[dict], year: Optional[int] = None) -> list[dict]:
    if not year:
        year = datetime.datetime.now().year

    filtered_activities = []
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_year = int(date.split("-")[0])
        if parsed_year != year:
            continue
        filtered_activities.append(activity)

    return filtered_activities

def generate_km_per_day_heatmap_data(activities: list[dict]):
    """Generates heatmap data for kilometers per day."""

    heatmap_arr = np.zeros((12, 31))
    for activity in activities:
        date = activity["start_date"].split("T")[0]

        parsed_distance = activity["distance"] / 1000
        parsed_month = int(date.split("-")[1]) - 1
        parsed_day = int(date.split("-")[2])

        heatmap_arr[parsed_month, parsed_day - 1] += parsed_distance
    return heatmap_arr


def calculate_total_distance(activities: list[dict]):
    """Calculates total distance in kilometers."""
    distance_sum = 0
    for activity in activities:
        parsed_distance = activity["distance"] / 1000
        distance_sum += parsed_distance
    return distance_sum

def calculate_streak(activities: list[dict], from_date: Optional[datetime.date] = None):
    """Calculates the streak of consecutive days with activities from a given date."""
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

def calculate_num_rides(activities: list[dict]):
    """Calculates the number of rides."""
    return len(activities)

def calculate_biggest_ride(activities: list[dict]):
    """Calculates the biggest ride"""

    biggest_ride_distance = 0
    for activity in activities:
        biggest_ride_distance = max(biggest_ride_distance, activity["distance"])

    return biggest_ride_distance

def calculate_longest_ride(activities: list[dict]):
    """Calculates the longest ride."""
    longest_ride = 0
    for activity in activities:
        longest_ride = max(longest_ride, activity["moving_time"])
    return longest_ride

def calculate_moving_time(activities: list[dict]):
    """Calculates the moving time."""

    moving_time = 0
    for activity in activities:
        parsed_moving_time = activity["moving_time"]
        moving_time += parsed_moving_time
    return moving_time

def generate_ride_length_binned_data(activities: list[dict]):
    """Generates binned ride length counts for bar plotting."""

    # Extract distances in km for the specified year
    distance_list = []
    for activity in activities:
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

def generate_monthly_distance_binned_data(activities: list[dict]):
    """Generates binned montly distance counts for bar plotting."""

    df = pd.DataFrame({
        "Distance Bin": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
        "Months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    })

    return df


if __name__ == '__main__':
    save_strava_activities()

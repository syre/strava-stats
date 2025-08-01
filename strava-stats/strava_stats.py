import datetime
from collections import defaultdict
from typing import Optional

import numpy as np
import pandas as pd

def get_strava_activities_years(activities: list[dict]) -> list[int]:
    years = set()
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_year = int(date.split("-")[0])
        years.add(parsed_year)

    return list(years)


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

def calculate_streak_from_date(activities: list[dict], from_date: Optional[datetime.date] = None):
    """Calculates the streak of consecutive days with activities from a given date."""
    if not from_date:
        from_date = datetime.datetime.now().date()

    streak = 0
    parsed_dates_dict = defaultdict(bool)

    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if parsed_date > from_date:
            continue
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

def calculate_elevation(activities: list[dict]):
    elevation = 0
    for activity in activities:
        parsed_elevation = activity["total_elevation_gain"]
        elevation += parsed_elevation
    return elevation

def calculate_ride_days(activities: list[dict]):
    parsed_dates_dict = {}

    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_dates_dict[date] = True
    return len(parsed_dates_dict.keys())

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

    distance_bins = [0] * 12
    for activity in activities:
        date = activity["start_date"].split("T")[0]
        parsed_month = int(date.split("-")[1])
        distance_bins[parsed_month-1] += activity["distance"] / 1000

    df = pd.DataFrame({
        "Distance Bin": distance_bins,
        "Months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    })

    return df

import os
import datetime
import requests
import json
import pathlib

from dotenv import load_dotenv

AUTH_ENDPOINT: str = "https://www.strava.com/oauth/token"
ACTIVITIES_ENDPOINT: str = "https://www.strava.com/api/v3/athlete/activities"

load_dotenv()

def get_access_token():
    """Gets an access token from the Strava API using refresh token """
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'f': 'json',
    }

    response = requests.post(AUTH_ENDPOINT, data=payload)
    json_response = response.json()
    access_token = json_response['access_token']
    return access_token


def get_activities(access_token: str, page=1):
    """Gets a page of activities from the Strava API """
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(ACTIVITIES_ENDPOINT, headers=headers, params={'page': page})
    response.raise_for_status()
    json_response = response.json()
    return json_response

def save_strava_activities(path: str = 'activities.json'):
    """Saves Strava activities to a JSON file."""
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
    activities = json.load(open(pathlib.Path(__file__).parent.resolve() / path, 'r'))
    if not activities:
        raise ValueError("No activities found in the JSON file.")
    return activities


if __name__ == '__main__':
    save_strava_activities()

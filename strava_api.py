import os
import requests
from dotenv import load_dotenv

AUTH_ENDPOINT: str = "https://www.strava.com/oauth/token"
ACTIVITIES_ENDPOINT: str = "https://www.strava.com/api/v3/athlete/activities"

load_dotenv()

def get_access_token():
    """ Get access token from the Strava API using refresh token """
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
    """ Get a page of activities from the Strava API """
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(ACTIVITIES_ENDPOINT, headers=headers, params={'page': page})
    response.raise_for_status()
    json_response = response.json()
    return json_response

import json
import logging
import os
import pathlib

import requests
from dotenv import load_dotenv

AUTH_ENDPOINT: str = "https://www.strava.com/oauth/token"
ACTIVITIES_ENDPOINT: str = "https://www.strava.com/api/v3/athlete/activities"

load_dotenv()

logger = logging.getLogger(__name__)

# Constants
MAX_PAGES = 100  # Reasonable limit to prevent infinite loops
PER_PAGE = 200  # Max allowed by Strava API


class StravaAPIError(Exception):
    """Custom exception for Strava API errors"""

    pass


def get_access_token() -> str:
    """Gets an access token from the Strava API using refresh token"""
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    # Validate environment variables
    if not all([client_id, client_secret, refresh_token]):
        raise StravaAPIError(
            "missing required environment variables: STRAVA_CLIENT_ID, "
            "STRAVA_CLIENT_SECRET, or STRAVA_REFRESH_TOKEN"
        )

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    try:
        response = requests.post(AUTH_ENDPOINT, data=payload)
        response.raise_for_status()
        json_response = response.json()
        access_token = json_response["access_token"]
        return access_token
    except requests.exceptions.RequestException as e:
        logger.exception("failed to get access token")
        raise StravaAPIError("failed to authenticate with Strava") from e
    except KeyError:
        logger.exception("access token not found in response")
        raise StravaAPIError("invalid response from Strava API - no access token")


def get_activities(access_token: str, page: int = 1) -> list[dict]:
    """Gets a page of activities from the Strava API"""
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(
            ACTIVITIES_ENDPOINT,
            headers=headers,
            params={"page": page, "per_page": PER_PAGE},
        )
        response.raise_for_status()
        json_response = response.json()
        logger.info(f"retrieved {len(json_response)} activities from page {page}")
        return json_response
    except requests.exceptions.RequestException as e:
        logger.exception(f"failed to get activities (page {page})")
        raise StravaAPIError("failed to fetch activities") from e


def save_strava_activities(path: str = "data/activities.json") -> list[dict]:
    """Saves Strava activities to a JSON file and return the activities."""
    logger.info("fetching strava activities...")
    access_token = get_access_token()
    activities_list = []

    # Fetch all pages of activities
    for page in range(1, MAX_PAGES + 1):
        activities = get_activities(access_token, page=page)

        if not activities:
            logger.info(f"no more activities found at page {page}")
            break

        activities_list.extend(activities)
        logger.info(f"fetched page {page}: {len(activities)} activities")

        # If we got fewer than PER_PAGE results, we're on the last page
        if len(activities) < PER_PAGE:
            logger.info("reached last page of activities")
            break

    # Ensure directory exists
    file_path = pathlib.Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to file using context manager
    with open(file_path, "w") as f:
        json.dump(activities_list, f)

    logger.info(f"saved {len(activities_list)} activities to {path}")
    return activities_list


def load_strava_activities(path: str = "data/activities.json") -> list[dict]:
    """Loads saved Strava activities from a JSON file."""
    file_path = pathlib.Path(__file__).parent / path

    if not file_path.exists():
        raise FileNotFoundError(f"activities file not found at {file_path}")

    with open(file_path, "r") as f:
        activities = json.load(f)

    if not activities:
        logger.warning(f"no activities found in {file_path}")
        raise ValueError(f"no activities found in the JSON file at {path}")

    logger.info(f"loaded {len(activities)} activities from {path}")
    return activities

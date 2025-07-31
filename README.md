
# Strava Stats

## Overview
Strava Stats is a Python script using the Strava API and Plotly Dash to generate various statistics and visualizations based on your Strava activities. It provides insights into your biking metrics.

## Requirements
A .env file with the following variables:
- STRAVA_CLIENT_ID
- STRAVA_CLIENT_SECRET
- STRAVA_REFRESH_TOKEN

Fetch the STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET from https://www.strava.com/settings/api

THE STRAVA_REFRESH_TOKEN can be obtained by running the following in a browser:
```
https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
```
Afterwards copy the "code" parameter from the URL and use it in the curl command below to get the refresh token.
```
curl -X POST \
  https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=YOUR_CODE \
  -d grant_type=authorization_code
```
Replace YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, and YOUR_CODE with your actual values.

## TODO
- Implement a filter toggling different sports
- Use a real relational database to store and analyze data
- Containerize it
- More visualizations

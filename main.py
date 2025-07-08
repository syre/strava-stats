import sys
from dash import Dash, html, dcc

from plots import (
    generate_km_per_day_over_year_heatmap,
    generate_ride_length_binned_over_year_plot
)
from strava_stats import (
    load_strava_activities,
    generate_distance_for_year,
    generate_streak_for_year,
    generate_num_rides_for_year,
    generate_moving_time_for_year
)

app = Dash()
app.title = "Strava Stats"

activities = load_strava_activities()

app.layout = html.Div(children=[
    html.H1(children='Strava Stats'),
    html.H2(children=f'Distance: {"%.2f"%(generate_distance_for_year(activities))} KM'),
    html.H2(children=f'Streak ⚡: {generate_streak_for_year(activities)} days'),
    html.H2(children=f'Rides: {generate_num_rides_for_year(activities)}'),
    html.H2(children=f"Duration: {"%.2f"%(generate_moving_time_for_year(activities)/60/60)} hours"),
    dcc.Graph(id="ride-length-binned-over-year-graph", figure=generate_ride_length_binned_over_year_plot(activities)),
    html.H2(children="Distance (KM) by date", style={'textAlign': 'center'}),
    dcc.Graph(
        id='km-per-day-over-year-graph',
        figure=generate_km_per_day_over_year_heatmap(activities),
    )
])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

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

app = Dash(external_scripts=["https://unpkg.com/@tailwindcss/browser@4"])
app.title = "Strava Stats"

activities = load_strava_activities()

app.layout = html.Div(children=[
    html.H1(children='Strava Stats', className="text-3xl font-bold justify-self-center w-100 mx-auto my-8 text-slate-700"),
    html.Div(
        children=[
            html.B(children=f'Distance: {"%.2f"%(generate_distance_for_year(activities))} KM', className="flex-1 p-4"),
            html.B(children=f'Streak ⚡: {generate_streak_for_year(activities)} days', className="flex-1 p-4"),
            html.B(children=f'Rides: {generate_num_rides_for_year(activities)}', className="flex-1 p-4"),
        ],
        className="flex w-screen"
    ),
    html.Div(
        children=[
            html.B(children=f"Duration: {"%.2f"%(generate_moving_time_for_year(activities)/60/60)} hours", className="flex-1 p-4"),
        ],
        className="flex w-screen"
    ),
    html.Div(
        children=[
            html.H2(children="Ride length", className="font-bold justify-self-center w-100 mx-auto"),
            dcc.Graph(id="ride-length-binned-over-year-graph", figure=generate_ride_length_binned_over_year_plot(activities)),
        ]
    ),
    html.Div(
        children=[
            html.H2(children="Distance (KM) by date", className="font-bold justify-self-center w-100 mx-auto"),
            dcc.Graph(
                id='km-per-day-over-year-graph',
                figure=generate_km_per_day_over_year_heatmap(activities),
            ),
        ]
    )
]
)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

from dash import Dash, html, dcc
import plotly.io as pio

from plots import (
    generate_km_per_day_over_year_heatmap,
    generate_ride_length_binned_over_year_plot
)
from strava_stats import (
    load_strava_activities,
    filter_strava_activities_by_year,
    calculate_total_distance,
    calculate_streak,
    calculate_num_rides,
    calculate_moving_time,
    calculate_biggest_ride,
    calculate_longest_ride_for_year
)
from templates import load_reds_template


activities = load_strava_activities()
activities = filter_strava_activities_by_year(activities)
pio.templates["reds"] = load_reds_template()
pio.templates.default = "reds"

app = Dash(external_scripts=["https://unpkg.com/@tailwindcss/browser@4"])
app.title = "Strava Stats"


app.layout = html.Div(children=[
    html.H1(children='Strava Stats', className="text-3xl font-bold justify-self-center text-center w-100 mx-auto my-8 text-slate-700"),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(children="Distance", className="text-lg font-semibold mb-2 text-red-700"),
                    html.Div(children=f'{"%.2f"%(calculate_total_distance(activities))} KM', className="text-sm text-gray-700"),
                ],
                className="flex-1 p-4"
            ),
            html.Div(
                children=[
                    html.Div(children="Streak ⚡", className="text-lg font-semibold mb-2 text-red-700"),
                    html.Div(children=f"{calculate_streak(activities)} days", className="text-sm text-gray-700"),
                ],
                className="flex-1 p-4"
            ),
            html.Div(
                children=[
                    html.Div(children="Rides", className="text-lg font-semibold mb-2 text-red-700"),
                    html.Div(children=f'{calculate_num_rides(activities)}', className="text-sm text-gray-700")
                ],
                className="flex-1 p-4"
            ),
            html.Div(
                children=[
                    html.Div(children="Duration", className="text-lg font-semibold mb-2 text-red-700"),
                    html.Div(children=f'{"%.2f"%(calculate_moving_time(activities)/60/60)} hours', className="text-sm text-gray-700")
                ],
                className="flex-1 p-4"
            ),
            html.Div(
                children=[
                    html.Div(children="Longest Ride", className="text-lg font-semibold mb-2 text-red-700"),
                    html.Div(children=f"{"%.2f"%(calculate_longest_ride_for_year(activities)/60/60)} hours", className="text-sm text-gray-700")
                ],
                className="flex-1 p-4"
            ),
            html.Div(
                children=[
                    html.Div(children="Biggest Ride", className="text-lg font-semibold mb-2 text-red-700"),
                    html.Div(children=f"{"%.2f"%(calculate_biggest_ride(activities)/1000)} KM", className="text-sm text-gray-700")
                ],
                className="flex-1 p-4"
            ),
        ],
        className="grid grid-cols-3 gap-4 max-w-4xl mx-auto"
    ),
    html.Div(
        children=[
            html.H2(children="Distance (KM) by date", className="font-bold justify-self-center text-center w-100 mx-auto text-slate-700"),
            dcc.Graph(
                id='km-per-day-over-year-graph',
                figure=generate_km_per_day_over_year_heatmap(activities),
            ),
        ]
    ),
    html.Div(
        children=[
            html.H2(children="Ride length", className="font-bold justify-self-center text-center w-100 mx-auto text-slate-700"),
            dcc.Graph(id="ride-length-binned-over-year-graph", figure=generate_ride_length_binned_over_year_plot(activities)),
        ]
    ),
]
)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

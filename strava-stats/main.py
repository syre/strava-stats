from datetime import datetime

from dash import Dash, html, dcc, Input, Output, callback
import plotly.io as pio

from plots import (
    generate_km_per_day_over_year_heatmap,
    generate_ride_length_binned_plot,
    generate_monthly_distance_binned_plot,
)
from strava_stats import (
    get_strava_activities_years,
    filter_strava_activities_by_year,
    calculate_total_distance,
    calculate_streak,
    calculate_num_rides,
    calculate_moving_time,
    calculate_biggest_ride,
    calculate_longest_ride,
    calculate_elevation,
    calculate_ride_days,
)
from strava_api import load_strava_activities
from templates import load_reds_template

pio.templates["reds"] = load_reds_template()
pio.templates.default = "reds"

app = Dash(external_scripts=["https://unpkg.com/@tailwindcss/browser@4"])
app.title = "Strava Stats 🚲"

activities = load_strava_activities()
AVAILABLE_YEARS = sorted(get_strava_activities_years(activities), key=str, reverse=True)
CURRENT_YEAR = datetime.now().date().year

@callback(
    Output('main-container', 'children'),
    Input('year-dropdown', 'value')
)
def update_main_container(year):
    activities = load_strava_activities()
    activities = filter_strava_activities_by_year(activities, year=year)
    return [
        html.Div(
            id='main-container',
            children=[
                html.Div(
                    children=[
                        html.H2("Distance (KM) by Date", className="text-lg font-semibold text-center text-red-700 mb-4"),
                        dcc.Graph(id='km-per-day-over-year-graph', figure=generate_km_per_day_over_year_heatmap(activities)),
                    ],
                    className="max-w-7xl mx-auto px-4 mb-8 rounded shadow"
                ),
                html.Div(
                    className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto px-4 mb-12",
                    children=[
                        html.Div(
                            className="grid grid-cols-1 md:grid-cols-2 gap-4",
                            children=[
                                html.Div([
                                    html.Div("Distance", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f'{calculate_total_distance(activities):.2f} KM', className="text-sm text-gray-700"),
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Current Streak", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f"{calculate_streak(activities)} days", className="text-sm text-gray-700"),
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Rides", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f'{calculate_num_rides(activities)}', className="text-sm text-gray-700")
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Ride Days", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f"{calculate_ride_days(activities)}", className="text-sm text-gray-700")
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Duration", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f'{calculate_moving_time(activities)/60/60:.2f} hours', className="text-sm text-gray-700")
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Longest Ride", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f"{calculate_longest_ride(activities)/60/60:.2f} hours", className="text-sm text-gray-700")
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Biggest Ride", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f"{calculate_biggest_ride(activities)/1000:.2f} KM", className="text-sm text-gray-700")
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                                html.Div([
                                    html.Div("Elevation", className="text-lg font-semibold mb-2 text-red-700"),
                                    html.Div(f"{calculate_elevation(activities):.2f} M", className="text-sm text-gray-700")
                                ], className="p-4 shadow rounded flex flex-col justify-center text-center"),
                            ]
                        ),

                        html.Div(
                            children=[
                                html.H2("Ride Count By Length", className="text-lg font-semibold text-center text-red-700 mb-4"),
                                dcc.Graph(
                                    id="ride-length-binned-over-year-graph",
                                    figure=generate_ride_length_binned_plot(activities),
                                    style={"height": "300px"}
                                )
                            ],
                            className="bg-white p-4 rounded shadow overflow-hidden"
                        ),
                        html.Div(
                            children=[
                                html.H2("Monthly Distance", className="text-lg font-semibold text-center text-red-700 mb-4"),
                                dcc.Graph(
                                    id="monthly-distance-graph-graph",
                                    figure=generate_monthly_distance_binned_plot(activities),
                                    style={"height": "300px"}
                                )
                            ],
                            className="bg-white p-4 rounded shadow overflow-hidden"
                        )
                    ]
                )]
        )
]

app.layout = html.Div(children=[
    html.H1(
        "Strava Stats 🚲",
        className="text-3xl font-bold text-center w-full mx-auto my-8 text-slate-700"
    ),
    dcc.Dropdown(AVAILABLE_YEARS, CURRENT_YEAR, id='year-dropdown', className="my-8 w-32 mx-auto"),
    html.Div(id='main-container')],
)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

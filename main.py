import sys
from dash import Dash, html, dcc
import plotly.express as px

from strava_stats import (
    load_strava_activities,
    generate_km_per_day_over_year_heatmap_data,
    generate_km_year_to_date,
    generate_streak
)

activities = load_strava_activities()
if not activities:
    sys.exit("No activities found")

app = Dash()
app.title = "Strava Stats"
fig = px.imshow(
    generate_km_per_day_over_year_heatmap_data(activities),
    labels={"x": "Day", "y": "Month", "color": "Kilometers"},
    x=list(range(1, 32)),
    y=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    template="plotly_dark"
)


meters_this_year = 56958123

app.layout = html.Div(children=[
    html.H1(children='Strava Dashboard'),
    html.H2(children=f'Year-to-date: {"%.2f"%(generate_km_year_to_date(activities))} KM'),
    html.H2(children=f'Streak ⚡: {generate_streak(activities)} days'),
    html.H2(children="KM per day", style={'textAlign': 'center'}),
    dcc.Graph(
        id='km-pear-day-over-year-graph',
        figure=fig,
    )
])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

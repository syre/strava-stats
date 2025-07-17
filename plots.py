import plotly.express as px

from strava_stats import (
    generate_km_per_day_over_year_heatmap_data,
    generate_ride_length_binned_over_year_data,
)

def generate_km_per_day_over_year_heatmap(activities):
    data = generate_km_per_day_over_year_heatmap_data(activities)
    fig = px.imshow(
        data,
        labels={"x": "Day", "y": "Month", "color": "Kilometers"},
        x=list(range(1, 32)),
        y=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        text_auto=".2f",
        template="plotly_dark",
        aspect="auto"
    )
    fig.update_xaxes(side="top", type="category")
    return fig


def generate_ride_length_binned_over_year_plot(activities, year=None):
    data = generate_ride_length_binned_over_year_data(activities, year)
    fig = px.bar(
        data,
        x="Count",
        y="Distance Bin",
        orientation="h",
        labels={"Count": "Number of Rides", "Distance Bin": "Distance (km)"},
        template="plotly_dark"
    )
    fig.update_layout(
        yaxis=dict(categoryorder="array", categoryarray=data["Distance Bin"]),
        bargap=0.1
    )
    return fig

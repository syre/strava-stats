import plotly.express as px

from strava_stats import (
    generate_km_per_day_heatmap_data,
    generate_ride_length_binned_data,
    generate_monthly_distance_binned_data,
)

def generate_km_per_day_over_year_heatmap(activities):
    data = generate_km_per_day_heatmap_data(activities)
    fig = px.imshow(
        data,
        labels={"x": "Day", "y": "Month", "color": "Kilometers"},
        x=list(range(1, 32)),
        y=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="reds"
    )
    fig.update_xaxes(side="top", type="category")
    fig.update_coloraxes(showscale=False)
    fig.update_layout(yaxis_title=None, margin_pad=5)
    return fig


def generate_ride_length_binned_plot(activities):
    data = generate_ride_length_binned_data(activities)
    fig = px.bar(
        data,
        x="Count",
        y="Distance Bin",
        orientation="h",
        labels={"Count": "Number of Rides", "Distance Bin": "Distance (km)"},
    )
    fig.update_layout(
        yaxis=dict(categoryorder="array", categoryarray=data["Distance Bin"]),
        bargap=0.1
    )
    return fig

def generate_monthly_distance_binned_plot(activities):
    data = generate_monthly_distance_binned_data(activities)
    fig = px.bar(
        data,
        x="Months",
        y="Distance Bin",
        labels={"Months": "Months", "Distance Bin": "Distance (km)"},
    )
    fig.update_layout(
        yaxis=dict(categoryorder="array", categoryarray=data["Distance Bin"]),
        xaxis_title=None,
        bargap=0.1
    )
    return fig

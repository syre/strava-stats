import plotly.express as px
import numpy as np
from strava_stats.strava_stats import (
    generate_km_per_day_heatmap_data,
    generate_ride_length_binned_data,
    generate_monthly_distance_binned_data,
)

def generate_km_per_day_over_year_heatmap(activities: list[dict], color="reds"):
    data = generate_km_per_day_heatmap_data(activities)

    fig = px.imshow(
        data,
        labels={"x": "Day", "y": "Month", "color": "Kilometers"},
        x=list(range(1, 32)),
        y=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        text_auto=False,
        aspect="auto",
        color_continuous_scale=color
    )

    zero_entry_text = np.where(np.logical_or(data == 0, np.isnan(data)), "", np.round(data, 2).astype(str))
    fig.update_traces(text=zero_entry_text, texttemplate="%{text}")
    fig.update_xaxes(side="top", type="category")
    fig.update_coloraxes(showscale=False)
    fig.update_layout(xaxis_title=None, yaxis_title=None, margin_pad=5, margin=dict(l=10, r=10, t=10, b=10))

    return fig


def generate_ride_length_binned_plot(activities: list[dict]):
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
        bargap=0.1,
        margin=dict(l=5, r=5, t=5, b=5),
    )

    return fig

def generate_monthly_distance_binned_plot(activities: list[dict]):
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
        bargap=0.1,
        margin=dict(l=5, r=5, t=5, b=5),
    )

    return fig

import plotly.io as pio
import plotly.express as px

def load_reds_template():
    reds_template = pio.templates["plotly_white"]  # Start from a clean base
    reds_template.layout.colorway = px.colors.sequential.Reds[2:]  # Skip lightest shades
    reds_template.layout.paper_bgcolor = "white"
    reds_template.layout.plot_bgcolor = "white"

    reds_template.layout.font = dict(
        family="Arial",
        size=14,
        color="black"
    )

    reds_template.layout.title = dict(
        font=dict(
            family="Arial",
            size=20,
            color="darkred"
        )
    )

    return reds_template


def load_reds_dark_template():
    reds_dark_template = pio.templates["plotly_dark"]  # Start from dark base
    reds_dark_template.layout.colorway = px.colors.sequential.Reds[2:]  # Skip lightest shades

    reds_dark_template.layout.paper_bgcolor = "black"
    reds_dark_template.layout.plot_bgcolor = "black"

    reds_dark_template.layout.font = dict(
        family="Arial",
        size=14,
        color="white"  # Contrast against dark background
    )

    reds_dark_template.layout.title = dict(
        font=dict(
            family="Arial",
            size=20,
            color="red"
        )
    )

    return reds_dark_template

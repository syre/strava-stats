from datetime import datetime

import plotly.io as pio
from dash import Dash, Input, Output, State, callback, dcc, html

from strava_stats.plots import (
    generate_km_per_day_over_year_heatmap,
    generate_monthly_distance_binned_plot,
    generate_ride_length_binned_plot,
)
from strava_stats.strava_api import load_strava_activities
from strava_stats.strava_stats import (
    calculate_biggest_ride,
    calculate_elevation,
    calculate_longest_ride,
    calculate_moving_time,
    calculate_num_rides,
    calculate_ride_days,
    calculate_streak_from_date,
    calculate_total_distance,
    filter_strava_activities,
    get_strava_activities_years,
)
from strava_stats.templates import load_reds_dark_template, load_reds_template

app = Dash(external_scripts=["https://unpkg.com/@tailwindcss/browser@4"])
app.title = "Strava Stats 🚲"

activities = load_strava_activities()
AVAILABLE_YEARS = sorted(get_strava_activities_years(activities), key=str, reverse=True)
CURRENT_YEAR = datetime.now().date().year

pio.templates["reds_dark"] = load_reds_dark_template()
pio.templates["reds_light"] = load_reds_template()


def get_theme_colors(is_dark: bool) -> dict:
    """Returns theme color configuration based on dark mode setting"""
    if is_dark:
        return {
            "bg_primary": "bg-zinc-950",
            "bg_secondary": "bg-zinc-900",
            "bg_card": "bg-zinc-900",
            "text_primary": "text-zinc-100",
            "text_secondary": "text-zinc-400",
            "text_accent": "text-red-500",
            "border": "border-zinc-800",
            "shadow": "shadow-lg shadow-zinc-950/50",
            "heatmap_color": "inferno",
            "template": "reds_dark",
        }
    else:
        return {
            "bg_primary": "bg-white",
            "bg_secondary": "bg-gray-50",
            "bg_card": "bg-white",
            "text_primary": "text-gray-900",
            "text_secondary": "text-gray-600",
            "text_accent": "text-red-700",
            "border": "border-gray-200",
            "shadow": "shadow-md",
            "heatmap_color": "reds",
            "template": "reds_light",
        }


def create_stat_card(title: str, value: str, theme_colors: dict) -> html.Div:
    """Creates a consistent stat card component"""
    return html.Div(
        [
            html.Div(
                title,
                className=f"text-sm font-semibold mb-1 {theme_colors['text_accent']}",
            ),
            html.Div(
                value,
                className=f"text-xl font-bold {theme_colors['text_primary']}",
            ),
        ],
        className=f"p-3 {theme_colors['bg_card']} {theme_colors['shadow']} rounded flex flex-col justify-center text-center border {theme_colors['border']} transition-transform duration-200",
    )


def create_chart_container(
    title: str, graph_id: str, figure, theme_colors: dict, height: str = "300px"
) -> html.Div:
    """Creates a consistent chart container component"""
    return html.Div(
        children=[
            html.H2(
                title,
                className=f"text-base font-bold text-center {theme_colors['text_accent']} mb-2",
            ),
            dcc.Graph(
                id=graph_id,
                figure=figure,
                style={"height": height},
                config={"displayModeBar": False},
            ),
        ],
        className=f"p-3 {theme_colors['bg_card']} rounded {theme_colors['shadow']} border {theme_colors['border']}",
    )


@callback(
    Output("dark-mode-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("dark-mode-store", "data"),
    prevent_initial_call=True,
)
def toggle_dark_mode(_, current_mode):
    """Toggle dark mode and save to cookie storage"""
    return not current_mode if current_mode is not None else True


@callback(
    [
        Output("main-container", "children"),
        Output("app-container", "className"),
        Output("header-container", "className"),
        Output("footer-container", "className"),
        Output("header-title", "className"),
    ],
    [
        Input("year-dropdown", "value"),
        Input("type-dropdown", "value"),
        Input("dark-mode-store", "data"),
    ],
)
def update_app(year, activity_type, is_dark):
    # Use dark mode from cookie storage
    if is_dark is None:
        is_dark = False
    theme_colors = get_theme_colors(is_dark)

    # set the appropriate plotly template
    pio.templates.default = theme_colors["template"]

    activities = load_strava_activities()
    activities = filter_strava_activities(
        activities, year=year, activity_type=activity_type
    )

    # update main content theme and children
    main_content = [
        html.Div(
            id="main-container-inner",
            children=[
                # Heatmap section
                html.Div(
                    children=[
                        html.H2(
                            "Distance (KM) by Date",
                            className=f"text-base font-bold text-center {theme_colors['text_accent']} mb-2",
                        ),
                        dcc.Graph(
                            id="km-per-day-over-year-graph",
                            figure=generate_km_per_day_over_year_heatmap(
                                activities, color=theme_colors["heatmap_color"]
                            ),
                            config={"displayModeBar": False},
                        ),
                    ],
                    className=f"max-w-7xl mx-auto px-2 mb-4 p-3 rounded {theme_colors['shadow']} {theme_colors['bg_card']} border {theme_colors['border']}",
                ),
                html.Div(
                    className="grid grid-cols-1 lg:grid-cols-3 gap-3 max-w-7xl mx-auto",
                    children=[
                        html.Div(
                            className="grid grid-cols-2 gap-2",
                            children=[
                                create_stat_card(
                                    "Distance",
                                    f"{calculate_total_distance(activities):.2f} KM",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Current Streak",
                                    f"{calculate_streak_from_date(activities)} days",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Rides",
                                    f"{calculate_num_rides(activities)}",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Ride Days",
                                    f"{calculate_ride_days(activities)}",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Duration",
                                    f"{calculate_moving_time(activities) / 60 / 60:.1f} hrs",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Longest Ride",
                                    f"{calculate_longest_ride(activities) / 60 / 60:.1f} hrs",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Biggest Ride",
                                    f"{calculate_biggest_ride(activities) / 1000:.2f} KM",
                                    theme_colors,
                                ),
                                create_stat_card(
                                    "Elevation",
                                    f"{calculate_elevation(activities):.0f} M",
                                    theme_colors,
                                ),
                            ],
                        ),
                        create_chart_container(
                            "Ride Count By Length",
                            "ride-length-binned-over-year-graph",
                            generate_ride_length_binned_plot(activities),
                            theme_colors,
                            "300px",
                        ),
                        create_chart_container(
                            "Monthly Distance",
                            "monthly-distance-graph-graph",
                            generate_monthly_distance_binned_plot(activities),
                            theme_colors,
                            "300px",
                        ),
                    ],
                ),
            ],
        )
    ]

    # update the theme of the rest of the classes in the app
    app_container_class = (
        f"{theme_colors['bg_primary']} min-h-screen transition-colors duration-300"
    )
    header_class = f"max-w-7xl mx-auto px-2 py-4 mb-4 {theme_colors['bg_secondary']} rounded-b {theme_colors['shadow']} border-b border-x {theme_colors['border']} transition-colors duration-300"
    footer_class = f"max-w-7xl mx-auto px-2 py-4 text-center {theme_colors['text_secondary']} text-xs mt-6 transition-colors duration-300"
    header_title_class = f"text-4xl font-bold {theme_colors['text_primary']} text-center flex-1 transition-colors duration-300"

    return (
        main_content,
        app_container_class,
        header_class,
        footer_class,
        header_title_class,
    )


app.layout = html.Div(
    id="app-container",
    className="bg-white min-h-screen transition-colors duration-300",
    children=[
        # Store for dark mode preference (stored in browser cookie/localStorage)
        dcc.Store(id="dark-mode-store", storage_type="local", data=False),
        # Header section
        html.Div(
            id="header-container",
            className="max-w-7xl mx-auto px-2 py-4 mb-4 bg-gray-50 rounded-b shadow-md border-b border-x border-gray-200 transition-colors duration-300",
            children=[
                html.Div(
                    className="flex justify-between items-center mb-3",
                    children=[
                        html.Div(className="w-24"),  # spacer for centering
                        html.H1(
                            "Strava Stats 🚲",
                            id="header-title",
                            className="text-4xl font-bold text-gray-900 text-center flex-1 transition-colors duration-300",
                        ),
                        html.Button(
                            "Light/Dark Mode",
                            id="theme-toggle",
                            n_clicks=0,
                            className="px-3 py-1 rounded bg-red-500 hover:bg-red-600 text-white text-sm font-medium transition-colors duration-200 cursor-pointer border-0 w-24",
                        ),
                    ],
                ),
                html.Div(
                    className="flex justify-center gap-4 flex-wrap",
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                AVAILABLE_YEARS,
                                CURRENT_YEAR,
                                id="year-dropdown",
                                className="w-32",
                                placeholder="Year",
                            ),
                        ),
                        html.Div(
                            dcc.Dropdown(
                                ["Ride", "Run", "Hike"],
                                "Ride",
                                id="type-dropdown",
                                className="w-32",
                                placeholder="Type",
                                disabled=True,
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # Main content
        html.Div(id="main-container"),
        # Footer
        html.Div(
            id="footer-container",
            className="max-w-7xl mx-auto px-2 py-4 text-center text-gray-600 text-xs mt-6",
            children=[
                html.P("Powered by Strava API"),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=True)

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from components.sidebar import create_sidebar
from pages import dashboard, options, pnl, chart

from components.callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
register_callbacks(app)

sidebar = create_sidebar()

content = html.Div(
    style={"margin-left": "18rem", "padding": "2rem"},
    children=[

        html.Div([
            html.H4(id="ticker-display"),

            dcc.Dropdown(
                id="timeframe-select",
                options=[
                    {"label": "1 Min", "value": "1m"},
                    {"label": "5 Min", "value": "5m"},
                    {"label": "15 Min", "value": "15m"},
                    {"label": "1 Hour", "value": "1h"},
                    {"label": "1 Day", "value": "1d"},
                ],
                value="1m",
                style={"width": "150px"}
            ),

            html.Div(id="live-price")

        ], 
        style={
            "display": "flex",
            "gap": "20px",
            "alignItems": "center",
            "borderBottom": "1px solid #1f2937",
            "marginBottom": "20px"
        }),

        html.Div(id="page-content")

    ]
)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id="strategy", options=[], value="call"),
    ], style={"display": "none"}),
    dcc.Interval(id="interval", interval=2000, n_intervals=0),
    dcc.Location(id="url"),
    dcc.Store(id="global-ticker", data="AAPL"),
    dcc.Store(id="timeframe", data="1m"),
    dcc.Interval(id="interval",interval=5000, n_intervals=0),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)

def render_page(pathname):
    if pathname == "/options":
        return options.layout
    elif pathname == "/pnl":
        return pnl.layout
    elif pathname == "/chart":
        return chart.layout
    else:
        return dashboard.layout

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)

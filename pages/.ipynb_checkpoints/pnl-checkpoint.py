from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.H2("Strategy Builder"),

    dbc.Row([
        dbc.Col([
            html.Label("Strategy"),
            dcc.Dropdown(
                id="strategy",
                options=[
                    {"label": "Call", "value": "call"},
                    {"label": "Put", "value": "put"},
                    {"label": "Bull Spread", "value": "bull_spread"}
                ],
                value="call"
            ),
            dcc.Dropdown(
                id="option-type",
                options=[
                    {"label": "Call", "value": "call"},
                    {"label": "Put", "value": "put"},
                    ],
                value="call",
                style={"marginBottom": "15px"}
            ),
        ], width=4),

        dbc.Col([
            html.Label("Strike"),
            dcc.Slider(
                id="strike",
                min=50,
                max=200,
                step=1,
                value=100,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=4),

        dbc.Col([
            html.Label("Premium"),
            dcc.Slider(
                id="premium",
                min=50,
                max=200,
                step=1,
                value=100,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=4),
    ], className="mb-4"),

    dcc.Graph(id="pnl-chart")

], fluid=True)

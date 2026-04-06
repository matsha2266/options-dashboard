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
            )
        ], width=4),

        dbc.Col([
            html.Label("Strike"),
            dcc.Slider(id="strike", min=50, max=200, value=100)
        ], width=4),

        dbc.Col([
            html.Label("Premium"),
            dcc.Slider(id="premium", min=1, max=20, value=5)
        ], width=4),
    ], className="mb-4"),

    dcc.Graph(id="pnl-chart")

], fluid=True)
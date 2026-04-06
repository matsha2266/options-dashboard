from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.H2("📈 Dashboard"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="greek-chart"), width=8),
        dbc.Col([
            dcc.Input(id="ticker", value="AAPL"),
            dcc.Dropdown(
                id="greek",
                options=[{"label": g, "value": g} for g in ["Delta","Gamma","Vega"]],
                value="Delta"
            )
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="price-chart")),
        dbc.Col(dcc.Graph(id="options-chart"))
    ])

])
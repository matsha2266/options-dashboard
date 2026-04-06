from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.H2("Price Chart"),

    dcc.Graph(
        id="full-price-chart",
        style={"height": "600px"}
    )

], fluid=True)
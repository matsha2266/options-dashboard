from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H2("Options Chain"),
    dcc.Graph(id="price-chart", figure={}),
    dcc.Graph(
        id="heatmap-chart",
        figure={},
        style={"height": "400px"}  
    )
])
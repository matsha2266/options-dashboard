from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.H2("Options Analytics"),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="vol-smile-chart", figure={}, style={"height": "350px"}),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="oi-chart", figure={}, style={"height": "300px"}),
            width=6,
            style={"padding": "0px"}
        ),
        dbc.Col(
            dcc.Graph(id="volume-chart", figure={}, style={"height": "300px"}),
            width=6,
            style={"padding": "0px"}
        )
    ])

], fluid=True)
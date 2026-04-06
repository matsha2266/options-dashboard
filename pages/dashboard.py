from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.H2("📈 Dashboard"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="greek",
                options=[{"label": g, "value": g} for g in ["Delta","Gamma","Vega"]],
                value="Delta",
                className="mb-3"
            )
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="greek-chart"),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="returns-chart"),
            width=6,
            style={"padding": "0px"}
        ),
        dbc.Col(
            dcc.Graph(id="options-chart"),
            width=6,
            style={"padding": "0px"}
        )
    ], style={"margin": "0px"})

], fluid=True)
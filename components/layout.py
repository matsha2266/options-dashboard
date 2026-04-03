from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([

        dbc.Row([
            dbc.Col(html.H2("📈 Options Dashboard", className="text-center mb-4"))
        ]),

        dbc.Row([

            dbc.Col([
                dbc.Card([
                    html.H5("Controls"),
                    dcc.Input(id="ticker", value="AAPL", debounce=True),
                    dcc.Dropdown(
                        id="greek",
                        options=[{"label": g, "value": g} for g in ["Delta","Gamma","Vega"]],
                        value="Delta"
                    )
                ])
            ], width=3),

            dbc.Col([
                dbc.Card([
                    dcc.Loading(dcc.Graph(id="greek-chart"))
                ])
            ], width=9)

        ]),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="price-chart")), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="options-chart")), width=6)
        ])

    ], fluid=True)

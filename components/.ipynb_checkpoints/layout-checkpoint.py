from dash import html, dcc

def create_layout():
    return html.Div([
        html.H1("Options Trading Dashboard", style={"textAlign":"center"}),

        dcc.Tabs([
            dcc.Tab(label="Greeks Visualizer", children=[
                html.Div([
                    dcc.Input(id="ticker", value="AAPL"),
                    dcc.Dropdown(
                        id="greek",
                        options=[{"label":g,"value":g} for g in ["Delta","Gamma","Vega"]],
                        value="Delta"
                    ),
                    dcc.Graph(id="greek-chart")
                ])
            ]),

            dcc.Tab(label="Options Chain", children=[
                html.Div([
                    dcc.Graph(id="options-table")
                ])
            ]),

            dcc.Tab(label="Stock Price", children=[
                dcc.Graph(id="price-chart")
            ])
        ])
    ])

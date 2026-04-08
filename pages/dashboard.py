from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.Div([
        html.P("Market Overview", style={
            "textTransform": "uppercase",
            "letterSpacing": "0.14em",
            "color": "#94a3b8",
            "marginBottom": "8px",
            "fontSize": "0.75rem"
        }),
        html.H2("Trading Dashboard", style={"marginBottom": "8px"}),
        html.P(
            "Track Greek sensitivity, return distributions, and options activity from one consolidated view.",
            style={"color": "#cbd5e1", "maxWidth": "760px", "marginBottom": "24px"}
        ),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="greek",
                options=[{"label": g, "value": g} for g in ["Delta","Gamma","Vega","Theta","Rho"]],
                value="Delta",
                className="dark-dropdown mb-3"
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

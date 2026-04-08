from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.Div([
        html.P("Options Flow", style={
            "textTransform": "uppercase",
            "letterSpacing": "0.14em",
            "color": "#94a3b8",
            "marginBottom": "8px",
            "fontSize": "0.75rem"
        }),
        html.H2("Options Analytics", style={"marginBottom": "8px"}),
        html.P(
            "Compare implied volatility shape, open interest concentration, and directional flow in the options chain.",
            style={"color": "#cbd5e1", "maxWidth": "760px", "marginBottom": "24px"}
        ),
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="vol-smile-chart", figure={}, style={"height": "350px"}),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="oi-chart", figure={}, style={"height": "380px"}),
            width=6,
            style={"padding": "0px"}
        ),
        dbc.Col(
            dcc.Graph(id="volume-chart", figure={}, style={"height": "380px"}),
            width=6,
            style={"padding": "0px"}
        )
    ])

], fluid=True)

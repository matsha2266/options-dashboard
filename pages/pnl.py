from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.Div([
        html.P("Scenario Modeling", style={
            "textTransform": "uppercase",
            "letterSpacing": "0.14em",
            "color": "#94a3b8",
            "marginBottom": "8px",
            "fontSize": "0.75rem"
        }),
        html.H2("Strategy Builder", style={"marginBottom": "8px"}),
        html.P(
            "Stress-test common option structures and see how payoff changes as strike and premium move.",
            style={"color": "#cbd5e1", "maxWidth": "760px", "marginBottom": "24px"}
        ),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Position"),
            dcc.Dropdown(
                id="option-type",
                className="dark-dropdown",
                options=[
                    {"label": "Long Call", "value": "call"},
                    {"label": "Long Put", "value": "put"},
                    {"label": "Short Call", "value": "short_call"},
                    {"label": "Short Put", "value": "short_put"},
                    {"label": "Bull Call Spread", "value": "bull_call_spread"},
                    {"label": "Bear Put Spread", "value": "bear_put_spread"},
                    {"label": "Long Straddle", "value": "long_straddle"},
                    {"label": "Long Strangle", "value": "long_strangle"},
                ],
                value="call",
                style={"marginBottom": "15px"}
            ),
        ], width=4),

        dbc.Col([
            html.Label("Strike"),
            dcc.Slider(
                id="strike",
                min=50,
                max=200,
                step=1,
                value=100,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=4),

        dbc.Col([
            html.Label("Premium"),
            dcc.Slider(
                id="premium",
                min=50,
                max=200,
                step=1,
                value=100,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=4),
    ], className="mb-4"),

    dcc.Graph(id="pnl-chart")

], fluid=True)

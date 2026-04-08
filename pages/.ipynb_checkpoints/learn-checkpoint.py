from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.H2("Chart Explanations", className="mb-4"),

    dcc.Dropdown(
        id="learn-dropdown",
        options=[
            {"label": "Candlestick Chart", "value": "candlestick"},
            {"label": "Volatility Smile", "value": "vol_smile"},
            {"label": "Open Interest", "value": "oi"},
            {"label": "Call vs Put Volume", "value": "volume"},
            {"label": "Returns Distribution", "value": "returns"},
            {"label": "PnL Chart", "value": "pnl"},
            {"label": "Option Greeks", "value": "greeks"}
        ],
        placeholder="Select a chart...",
        style={"marginBottom": "25px"}
    ),
    html.Div(
        dcc.Dropdown(
            id="greek-selector",
            options=[
                {"label": "Delta", "value": "Delta"},
                {"label": "Gamma", "value": "Gamma"},
                {"label": "Vega", "value": "Vega"},
                {"label": "Theta", "value": "Theta"},
            ],
            value="delta",
        ),
        id="greek-container",
        style={"display": "none", "marginBottom": "20px"}
    ),
    html.Div(
        id="learn-output",
        style={
            "background": "#111827",
            "padding": "20px",
            "borderRadius": "10px",
            "border": "1px solid #1f2937"
        }
    ),
    
    html.Div(id="learn-chart", style={"marginTop": "30px"})

], fluid=True)
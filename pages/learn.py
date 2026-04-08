from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.Div([
        html.P("Reference Guide", style={
            "textTransform": "uppercase",
            "letterSpacing": "0.14em",
            "color": "#94a3b8",
            "marginBottom": "8px",
            "fontSize": "0.75rem"
        }),
        html.H2("Chart Explanations", style={"marginBottom": "8px"}),
        html.P(
            "Use this page to understand what each chart is showing and why traders pay attention to it.",
            style={"color": "#cbd5e1", "maxWidth": "760px", "marginBottom": "24px"}
        ),
    ]),

    dcc.Dropdown(
        id="learn-dropdown",
        className="dark-dropdown",
        options=[
            {"label": "Candlestick Chart", "value": "candlestick"},
            {"label": "Volatility Smile", "value": "vol_smile"},
            {"label": "Options Chain", "value": "options_chain"},
            {"label": "Open Interest", "value": "oi"},
            {"label": "Call vs Put Volume", "value": "volume"},
            {"label": "Returns Distribution", "value": "returns"},
            {"label": "PnL Chart", "value": "pnl"},
            {"label": "Option Greeks", "value": "greeks"}
        ],
        value="candlestick",
        placeholder="Select a chart...",
        style={"marginBottom": "25px"}
    ),
    html.Div(
        dcc.Dropdown(
            id="greek-selector",
            className="dark-dropdown",
            options=[
                {"label": "Delta", "value": "Delta"},
                {"label": "Gamma", "value": "Gamma"},
                {"label": "Vega", "value": "Vega"},
                {"label": "Theta", "value": "Theta"},
                {"label": "Rho", "value": "Rho"},
            ],
            value="Delta",
        ),
        id="greek-container",
        style={"display": "none", "marginBottom": "20px"}
    ),
    html.Div(
        dcc.Dropdown(
            id="learn-pnl-selector",
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
        ),
        id="pnl-container",
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

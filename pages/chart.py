from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.Div([
        html.P("Price Action", style={
            "textTransform": "uppercase",
            "letterSpacing": "0.14em",
            "color": "#94a3b8",
            "marginBottom": "8px",
            "fontSize": "0.75rem"
        }),
        html.H2("Price Chart", style={"marginBottom": "8px"}),
        html.P(
            "Inspect the ticker’s candlestick structure across the selected timeframe with a full-width chart view.",
            style={"color": "#cbd5e1", "maxWidth": "760px", "marginBottom": "24px"}
        ),
    ]),

    dcc.Graph(
        id="full-price-chart",
        style={"height": "600px"}
    )

], fluid=True)

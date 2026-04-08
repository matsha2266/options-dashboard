from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    html.Div([
        html.Div([
            html.P("Greek Surfaces", style={
                "textTransform": "uppercase",
                "letterSpacing": "0.14em",
                "color": "#94a3b8",
                "marginBottom": "8px",
                "fontSize": "0.75rem"
            }),
            html.H2("2D and 3D Greek Heatmaps", style={"marginBottom": "8px"}),
            html.P(
                "Explore how each option Greek reacts to changes in underlying price and implied volatility.",
                style={"color": "#cbd5e1", "maxWidth": "760px", "marginBottom": "0"}
            ),
        ], style={"flex": "1"}),
        html.Div([
            html.Div([
                html.Label("Greek", style={"marginBottom": "8px", "color": "#cbd5e1"}),
                dcc.Dropdown(
                    id="greek-heatmap-select",
                    className="dark-dropdown",
                    options=[
                        {"label": "Delta", "value": "Delta"},
                        {"label": "Gamma", "value": "Gamma"},
                        {"label": "Vega", "value": "Vega"},
                        {"label": "Theta", "value": "Theta"},
                        {"label": "Rho", "value": "Rho"},
                    ],
                    value="Delta",
                    clearable=False
                )
            ], style={"minWidth": "220px", "flex": "1"}),
            html.Div([
                html.Label("Colorway", style={"marginBottom": "8px", "color": "#cbd5e1"}),
                dcc.Dropdown(
                    id="greek-colorscale-select",
                    className="dark-dropdown",
                    options=[
                        {"label": "Earth", "value": "Earth"},
                        {"label": "Spectral", "value": "Turbo"},
                        {"label": "Red/Green", "value": "RdYlGn"},
                        {"label": "Viridis", "value": "Viridis"},
                        {"label": "Ice/Fire", "value": "IceFire"},
                        {"label": "Plasma", "value": "Plasma"},
                    ],
                    value="Earth",
                    clearable=False
                )
            ], style={"minWidth": "220px", "flex": "1"})
        ], style={"minWidth": "460px", "display": "flex", "gap": "16px", "flexWrap": "wrap"})
    ], style={
        "display": "flex",
        "gap": "24px",
        "justifyContent": "space-between",
        "alignItems": "end",
        "marginBottom": "24px",
        "flexWrap": "wrap"
    }),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("2D Heatmap", style={
                    "fontWeight": "600",
                    "marginBottom": "12px",
                    "color": "#f8fafc"
                }),
                dcc.Graph(
                    id="greek-heatmap-2d",
                    config={"responsive": True},
                    style={"height": "520px"}
                )
            ], style={
                "background": "linear-gradient(180deg, #111827 0%, #0f172a 100%)",
                "border": "1px solid #1f2937",
                "borderRadius": "16px",
                "padding": "16px",
                "boxShadow": "0 18px 40px rgba(0, 0, 0, 0.22)"
            })
        ], lg=6, xs=12),
        dbc.Col([
            html.Div([
                html.Div("3D Surface", style={
                    "fontWeight": "600",
                    "marginBottom": "12px",
                    "color": "#f8fafc"
                }),
                dcc.Graph(
                    id="greek-heatmap-3d",
                    config={"responsive": True},
                    style={"height": "520px"}
                )
            ], style={
                "background": "linear-gradient(180deg, #111827 0%, #0f172a 100%)",
                "border": "1px solid #1f2937",
                "borderRadius": "16px",
                "padding": "16px",
                "boxShadow": "0 18px 40px rgba(0, 0, 0, 0.22)"
            })
        ], lg=6, xs=12),
    ], className="g-4"),

], fluid=True)

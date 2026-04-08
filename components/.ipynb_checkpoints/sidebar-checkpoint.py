from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    return html.Div([

        html.H4("Menu", className="text-white"),

        dcc.Input(
            id="ticker-input",
            className="ticker-input",
            value="AAPL",
            debounce=True,
            style={
                "width": "100%",
                "margin-bottom": "10px",
                "color": "#f9fafb",
                "borderRadius": "6px"
            }
        ),

        dbc.Nav([
            dbc.NavLink("Dashboard", href="/", active="exact"),
            dbc.NavLink("Options Analytics", href="/options", active="exact"),
            dbc.NavLink("PnL Strategy Builder", href="/pnl", active="exact"),
            dbc.NavLink("Price Chart", href="/chart", active="exact"),
            dbc.NavLink("Learn", href="/learn", active="exact"),
        ], vertical=True, pills=True)

    ], style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#111827"
    })

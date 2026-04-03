from dash import Dash
import dash_bootstrap_components as dbc

from components.layout import create_layout
from components.callbacks import register_callbacks

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG]
)

app.layout = create_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)

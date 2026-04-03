from dash import Input, Output
from data.market_data import get_stock_price, get_price_history, get_options_chain
from components.charts import greek_curve, price_chart, options_chart

def register_callbacks(app):

    @app.callback(
        Output("greek-chart","figure"),
        Input("ticker","value"),
        Input("greek","value")
    )
    def update_greek(ticker, greek):
        S = get_stock_price(ticker)
        return greek_curve(S, S, 1, 0.05, 0.2, greek)

    @app.callback(
        Output("price-chart","figure"),
        Input("ticker","value")
    )
    def update_price(ticker):
        df = get_price_history(ticker)
        return price_chart(df)

    @app.callback(
        Output("options-chart","figure"),
        Input("ticker","value")
    )
    def update_options(ticker):
        calls, _ = get_options_chain(ticker)
        if calls is None:
            return {}
        return options_chart(calls.head(20))

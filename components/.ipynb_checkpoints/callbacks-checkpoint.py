from dash import Input, Output
from data.market_data import get_stock_price, get_options_chain
from components.charts import greek_curve
import plotly.express as px

def register_callbacks(app):

    @app.callback(
        Output("greek-chart","figure"),
        Input("ticker","value"),
        Input("greek","value")
    )
    def update_greek_chart(ticker, greek):
        S = get_stock_price(ticker)
        return greek_curve(S, S, 1, 0.05, 0.2, greek)

    @app.callback(
        Output("options-table","figure"),
        Input("ticker","value")
    )
    def update_options_chain(ticker):
        calls, _ = get_options_chain(ticker)
        if calls is None:
            return {}

        return px.bar(calls.head(10), x="strike", y="lastPrice", title="Options Chain")

    @app.callback(
        Output("price-chart","figure"),
        Input("ticker","value")
    )
    def update_price_chart(ticker):
        import yfinance as yf
        df = yf.Ticker(ticker).history(period="1mo")

        return px.line(df, x=df.index, y="Close", title="Stock Price")
from dash import Input, Output, html
from dash.exceptions import PreventUpdate
from data.market_data import get_stock_price, get_price_history, get_options_chain
from components.charts import greek_curve, price_chart, options_chart, pnl_chart, volatility_smile, open_interest_chart, returns_chart, volume_comparison
import yfinance as yf

def register_callbacks(app):

    # sync ticker input to global store
    @app.callback(
        Output("global-ticker", "data"),
        Input("ticker-input", "value"),
        Input("interval","n_intervals")
    )
    def update_global_ticker(ticker, n_intervals):
        return ticker if ticker else "AAPL"

    # display ticker in header
    @app.callback(
        Output("ticker-display","children"),
        Input("global-ticker","data"),
        Input("interval","n_intervals")
    )
    def show_ticker(ticker, n_intervals):
        return f"Ticker: {ticker}"

    # greeks chart
    @app.callback(
        Output("greek-chart","figure"),
        Input("global-ticker","data"),
        Input("greek","value"),
        Input("interval","n_intervals")
    )
    def update_greek(ticker, greek, n_intervals):
        try:
            if not ticker:
                ticker = "AAPL"
                
            S = get_stock_price(ticker)
            return greek_curve(S, S, 1, 0.05, 0.2, greek)
        except:
            return {}

    # price chart
    @app.callback(
        Output("price-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_price(ticker, timeframe, n):
        df = get_price_history(ticker, timeframe)
        return price_chart(df)

    # options chart
    @app.callback(
        Output("options-chart","figure"),
        Input("global-ticker","data"),
        Input("interval","n_intervals")
    )
    def update_options(ticker, n_intervals):
        try:
            if not ticker:
                ticker = "AAPL"
                
            calls, _ = get_options_chain(ticker)
            if calls is None:
                return {}
            return options_chart(calls.head(20))
        except:
            return {}

    # pnL chart

    @app.callback(
        Output("pnl-chart","figure"),
        Input("strategy","value"),
        Input("strike","value"),
        Input("premium","value"),
    )
    def update_pnl(strategy, strike, premium):
        if strategy is None:
            raise PreventUpdate

        return pnl_chart(strategy, strike, premium)
            
    # Live ticker
    @app.callback(
        Output("live-price","children"),
        Input("global-ticker","data"),
        Input("interval","n_intervals")
    )
    def update_live_price(ticker, n):
        try:
            if not ticker:
                ticker = "AAPL"

            stock = yf.Ticker(ticker)

            hist = stock.history(period="2d", interval="1d")

            if hist is None or hist.empty or "Close" not in hist:
                print("BAD HIST:", hist)
                return "N/A"

            if len(hist) < 2:
                return "N/A"

            price = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2]

            if price is None or prev is None:
                return "N/A"

            change = price - prev
            pct = (change / prev) * 100 if prev != 0 else 0

            is_up = change >= 0
            color = "#00ff99" if is_up else "#ff4d4d"

            return html.Div([
                html.Span(f"${price:.2f}", style={"fontSize": "20px", "fontWeight": "bold"}),
                html.Span(
                    f" {'▲' if is_up else '▼'} {change:.2f} ({pct:.2f}%)",
                    style={"color": color, "marginLeft": "10px"}
                )
            ])

        except Exception as e:
            print("LIVE PRICE ERROR:", e)
            return "N/A"

    
    @app.callback(
        Output("vol-smile-chart","figure"),
        Input("global-ticker","data")
    )
    def update_vol_smile(ticker):
        calls, _ = get_options_chain(ticker)
        return volatility_smile(calls)

    
    @app.callback(
        Output("oi-chart","figure"),
        Input("global-ticker","data")
    )
    def update_oi(ticker):
        calls, _ = get_options_chain(ticker)
        return open_interest_chart(calls)


    @app.callback(
        Output("volume-chart","figure"),
        Input("global-ticker","data")
    )
    def update_volume(ticker):
        calls, puts = get_options_chain(ticker)
        return volume_comparison(calls, puts)

    
    @app.callback(
        Output("returns-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data")
    )
    def update_returns(ticker, timeframe):
        df = get_price_history(ticker, timeframe)
        return returns_chart(df)

    
    @app.callback(
        Output("pnl-values","children"),
        Input("spot","value"),
        Input("strike","value"),
        Input("premium","value")
    )
    def show_values(s, k, p):
        return html.Div([
            html.Span(f"Spot: {s}", style={"marginRight": "20px"}),
            html.Span(f"Strike: {k}", style={"marginRight": "20px"}),
            html.Span(f"Premium: {p}")
        ])


    @app.callback(
        Output("full-price-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_full_chart(ticker, timeframe, n):
        df = get_price_history(ticker, timeframe)
        return price_chart(df)

    
    @app.callback(
        Output("timeframe","data"),
        Input("timeframe-select","value")
    )
    def update_timeframe(tf):
        return tf
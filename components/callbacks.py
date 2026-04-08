from dash import Input, Output, html, dcc
import plotly.graph_objects as go
from data.market_data import get_stock_price, get_price_history, get_options_chain
from components.charts import greek_curve, greek_heatmap, greek_surface, price_chart, options_chart, pnl_chart, volatility_smile, open_interest_chart, returns_chart, volume_comparison

chart_explanations = {
    "candlestick": {
        "title": "Candlestick Chart",
        "overview": "A candlestick chart compresses open, high, low, and close into one shape for each time bucket, so you can read both direction and intraperiod struggle at a glance.",
        "parts": [
            "Body: the filled middle section between the open and close. A rising body means the market closed above where it opened; a falling body means it closed below.",
            "Upper wick: shows how high price traded above the body before pulling back. Long upper wicks often suggest rejection from higher prices.",
            "Lower wick: shows how far price traded below the body before recovering. Long lower wicks often suggest buying support or rejection of lower prices.",
            "Series of candles: one candle is context, but sequences reveal trend, pause, breakout, exhaustion, and reversal behavior."
        ],
        "reading": [
            "Long bodies usually mean stronger conviction because price traveled more decisively during that interval.",
            "Small bodies with long wicks usually mean indecision, conflict, or failed attempts to push price further.",
            "Compression followed by larger candles often signals a transition from balance to expansion."
        ],
        "summary": "Candlesticks are best for reading trend, rejection, momentum, and volatility inside each interval."
    },
    "vol_smile": {
        "title": "Volatility Smile",
        "overview": "A volatility smile maps implied volatility across strikes, showing where the market is pricing options richly or cheaply relative to the rest of the chain.",
        "parts": [
            "X-axis: strike price, which tells you how far each option sits from the current underlying price.",
            "Y-axis: implied volatility, which reflects how much uncertainty or premium the market is pricing into that strike.",
            "Curve shape: the bend or skew of the line shows whether upside or downside protection is carrying a larger volatility premium."
        ],
        "reading": [
            "A steeper smile often means traders are paying more for tail protection, usually during uncertainty or event risk.",
            "If downside strikes carry noticeably higher IV than upside strikes, that usually reflects bearish skew or stronger demand for puts.",
            "Flat smiles suggest a more even volatility surface, while sharp dislocations can point to relative mispricing."
        ],
        "summary": "Use the smile to read skew, tail-risk demand, and where the market is assigning the highest volatility premium."
    },
    "options_chain": {
        "title": "Options Chain",
        "overview": "An options chain graph compares option prices across strikes, giving you a quick view of where premiums concentrate as contracts move in or out of the money.",
        "parts": [
            "X-axis: strike price for each option in the selected expiration.",
            "Y-axis: last traded option price, which reflects the market premium attached to that strike.",
            "Bar heights: show which strikes are carrying the highest dollar premium at the moment.",
            "Shape across strikes: helps show where premium decays and where the chain is most active or expensive."
        ],
        "reading": [
            "Higher premiums near key strikes usually reflect more intrinsic value, more time value, or both.",
            "A steep drop-off across strikes often shows where contracts move further out of the money and become cheaper quickly.",
            "This chart is best read as a pricing snapshot, not a direction signal by itself."
        ],
        "summary": "Use the options chain chart to compare premium levels across strikes and spot where the market is assigning the most option value."
    },
    "oi": {
        "title": "Open Interest",
        "overview": "Open interest shows how many contracts remain open at each strike, making it a positioning map rather than a flow map.",
        "parts": [
            "Bar height: the number of still-open contracts at a strike, not just trades that happened today.",
            "Strike clusters: areas where several nearby strikes all have large open interest often matter more than a single isolated spike.",
            "Distribution shape: the full spread of bars shows where participants have concentrated exposure across the chain."
        ],
        "reading": [
            "Large open-interest zones can act as attention magnets because hedging and positioning are concentrated there.",
            "They are often watched as possible support, resistance, or expiration pinning areas, especially when price drifts nearby.",
            "Open interest is not directional by itself; it tells you where size sits, not whether traders are bullish or bearish."
        ],
        "summary": "Open interest helps identify crowded strikes, likely liquidity pockets, and areas where dealer hedging may matter."
    },
    "volume": {
        "title": "Call vs Put Volume",
        "overview": "This chart compares how much call volume traded versus put volume, giving a fast view of current options flow and sentiment tilt.",
        "parts": [
            "Call bar: total call contracts traded, which can reflect bullish speculation, covered-call activity, or upside hedging.",
            "Put bar: total put contracts traded, which can reflect bearish trades, downside hedging, or protection buying.",
            "Imbalance: the gap between the bars tells you how strongly flow leaned in one direction."
        ],
        "reading": [
            "A call-heavy session often signals more upside participation or risk-taking.",
            "A put-heavy session often signals more caution, protection demand, or bearish speculation.",
            "Volume is today's flow, not ongoing inventory, so it should be read differently from open interest."
        ],
        "summary": "Use call-versus-put volume as a quick flow and sentiment snapshot, especially when paired with open interest."
    },
    "returns": {
        "title": "Returns Distribution",
        "overview": "A returns distribution shows how often different price changes occurred, helping you understand realized volatility and the shape of risk.",
        "parts": [
            "Center mass: where most bars cluster, representing the move sizes that happen most often.",
            "Spread: the overall width of the histogram, which tells you how variable returns have been.",
            "Tails: the far-left and far-right bars, which represent rare but important extreme outcomes."
        ],
        "reading": [
            "A narrow distribution suggests more stable movement over the selected timeframe.",
            "A wider distribution suggests more violent or inconsistent price changes.",
            "Heavy tails mean outsized moves happen more often than a simple normal-risk assumption would suggest."
        ],
        "summary": "This chart is useful for understanding typical move size, volatility regime, and how much tail risk is hiding in the series."
    },
    "pnl": {
        "title": "PnL Chart",
        "overview": "A PnL chart plots the strategy payoff at expiration across a range of underlying prices so you can see the full trade shape before entering it.",
        "parts": [
            "X-axis: possible underlying prices at expiration.",
            "Y-axis: resulting profit or loss for the selected strategy at each price point.",
            "Zero line: where the payoff crosses this line is your breakeven level.",
            "Curve shape: the slope and curvature reveal whether risk is capped, open-ended, symmetric, or convex."
        ],
        "reading": [
            "Convex shapes usually indicate long optionality because gains can accelerate once price moves enough.",
            "Flat or capped regions often show where another option leg starts offsetting additional gains or losses.",
            "The downside and upside endpoints help you quickly judge whether a strategy is limited-risk or carries open-ended exposure."
        ],
        "summary": "Use the PnL chart to read breakevens, capped versus uncapped payoff, and the trade’s risk-reward geometry."
    },
    "greeks": {
        "title": "Option Greeks",
        "overview": "The Greeks describe how an option responds to changes in price, time, volatility, and rates. They are the main language of option risk management.",
        "parts": [
            "Delta: expected change in option value for a $1 move in the underlying.",
            "Gamma: rate of change of Delta, showing how quickly directional exposure can shift.",
            "Theta: time decay, or how much value tends to erode as expiration gets closer.",
            "Vega: sensitivity to changes in implied volatility.",
            "Rho: sensitivity to interest-rate changes, usually less important for short-dated equity options than the others."
        ],
        "reading": [
            "High absolute Delta means the option behaves more like stock exposure.",
            "High Gamma means positioning can change quickly, especially around the strike.",
            "Large negative Theta means time is working against long premium positions more aggressively.",
            "High Vega means the option is very exposed to volatility expansion or contraction."
        ],
        "summary": "The Greeks work together as a live risk dashboard for direction, convexity, decay, and volatility exposure."
    }
}


def _placeholder_figure(title, message):
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        title=title,
        annotations=[{
            "text": message,
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": 0.5,
            "showarrow": False,
            "font": {"color": "white"}
        }]
    )
    return fig

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

    @app.callback(
        Output("greek-heatmap-2d", "figure"),
        Output("greek-heatmap-3d", "figure"),
        Input("global-ticker", "data"),
        Input("greek-heatmap-select", "value"),
        Input("greek-colorscale-select", "value"),
        Input("timeframe", "data"),
        Input("interval", "n_intervals")
    )
    def update_greek_heatmap_page(ticker, greek, colorscale, timeframe, n_intervals):
        try:
            ticker = ticker or "AAPL"
            df = get_price_history(ticker, timeframe or "1m")
            if df is not None and not df.empty and "Close" in df:
                S = df["Close"].iloc[-1]
            else:
                S = get_stock_price(ticker)
            return (
                greek_heatmap(S, S, 1, 0.05, 0.2, greek, colorscale or "RdYlGn"),
                greek_surface(S, S, 1, 0.05, 0.2, greek, colorscale or "Earth")
            )
        except Exception:
            return {}, {}

    # greeks chart
    @app.callback(
        Output("greek-chart","figure"),
        Input("global-ticker","data"),
        Input("greek","value"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_greek(ticker, greek, timeframe, n_intervals):
        try:
            if not ticker:
                ticker = "AAPL"

            df = get_price_history(ticker, timeframe or "1m")
            if df is not None and not df.empty and "Close" in df:
                S = df["Close"].iloc[-1]
            else:
                S = get_stock_price(ticker)
            return greek_curve(S, S, 1, 0.05, 0.2, greek)
        except:
            return {}

    # options chart
    @app.callback(
        Output("options-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_options(ticker, timeframe, n_intervals):
        try:
            if not ticker:
                ticker = "AAPL"

            calls, _ = get_options_chain(ticker)
            if calls is None:
                return {}
            spot = get_stock_price(ticker) or calls["strike"].median()
            nearby = calls.copy()
            nearby["distance"] = (nearby["strike"] - spot).abs()
            nearby = nearby.nsmallest(20, "distance").sort_values("strike")
            return options_chart(nearby)
        except:
            return {}

    # pnL chart
    @app.callback(
        Output("pnl-chart","figure"),
        Input("option-type","value"),
        Input("strike","value"),
        Input("premium","value")
    )
    def update_pnl(option_type, strike, premium):
        return pnl_chart(option_type, strike, premium)     
        
    # Live ticker
    @app.callback(
        Output("live-price","children"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_live_price(ticker, timeframe, n):
        try:
            if not ticker:
                ticker = "AAPL"

            intraday = get_price_history(ticker, "1m")
            hist = intraday if intraday is not None and not intraday.empty else get_price_history(ticker, "1d")

            if hist is None or hist.empty or "Close" not in hist:
                return "N/A"

            if "Open" not in hist:
                return "N/A"

            price = hist["Close"].iloc[-1]
            market_open = hist["Open"].iloc[0]

            if price is None or market_open is None:
                return "N/A"

            change = price - market_open
            pct = (change / market_open) * 100 if market_open != 0 else 0

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
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_vol_smile(ticker, timeframe, n_intervals):
        try:
            calls, puts = get_options_chain(ticker or "AAPL")
            spot = get_stock_price(ticker or "AAPL")
            return volatility_smile(calls, puts, spot)
        except Exception:
            return _placeholder_figure("Volatility Smile", "Unable to load implied volatility data")

    
    @app.callback(
        Output("oi-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_oi(ticker, timeframe, n_intervals):
        try:
            calls, puts = get_options_chain(ticker or "AAPL")
            spot = get_stock_price(ticker or "AAPL")
            return open_interest_chart(calls, puts, spot)
        except Exception:
            return _placeholder_figure("Open Interest by Strike", "Unable to load open interest data")


    @app.callback(
        Output("volume-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_volume(ticker, timeframe, n_intervals):
        try:
            calls, puts = get_options_chain(ticker or "AAPL")
            return volume_comparison(calls, puts)
        except Exception:
            return _placeholder_figure("Call vs Put Volume", "Unable to load options volume data")

    
    @app.callback(
        Output("returns-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_returns(ticker, timeframe, n_intervals):
        try:
            df = get_price_history(ticker or "AAPL", timeframe or "1m")
            return returns_chart(df)
        except Exception:
            return _placeholder_figure("Returns Distribution", "Unable to load return history")


    @app.callback(
        Output("full-price-chart","figure"),
        Input("global-ticker","data"),
        Input("timeframe","data"),
        Input("interval","n_intervals")
    )
    def update_full_chart(ticker, timeframe, n):
        try:
            df = get_price_history(ticker or "AAPL", timeframe or "1m")
            return price_chart(df)
        except Exception:
            return _placeholder_figure("Price Chart", "Unable to load price history")

    
    @app.callback(
        Output("timeframe","data"),
        Input("timeframe-select","value")
    )
    def update_timeframe(tf):
        return tf or "1m"

    @app.callback(
        Output("learn-output", "children"),
        Input("learn-dropdown", "value")
    )
    def update_learn(selection):
        if not selection:
            return "Select a chart to see explanation."

        data = chart_explanations.get(selection)
        if not data:
            return "Explanation unavailable."

        return [
            html.H4(data["title"], style={"marginBottom": "15px"}),
            html.P(data["overview"], style={"color": "#d1d5db", "lineHeight": "1.7", "marginBottom": "16px"}),
            html.Hr(),
            html.H5("What The Parts Mean", style={"marginBottom": "10px", "fontSize": "1rem"}),
            html.Ul([
                html.Li(point, style={"marginBottom": "8px"}) for point in data["parts"]
            ], style={"marginBottom": "18px"}),
            html.H5("How To Read It", style={"marginBottom": "10px", "fontSize": "1rem"}),
            html.Ul([
                html.Li(point, style={"marginBottom": "8px"}) for point in data["reading"]
            ]),
            html.P(
                f"Summary: {data['summary']}",
                style={"fontWeight": "bold", "marginTop": "10px"}
            )
        ]
        

    @app.callback(
        Output("learn-chart", "children"),
        Input("learn-dropdown", "value"),
        Input("global-ticker", "data"),
        Input("timeframe", "data"),
        Input("greek-selector", "value"),
        Input("learn-pnl-selector", "value"),
        Input("interval", "n_intervals")
    )
    def update_learn_chart(selection, ticker, timeframe, greek, pnl_strategy, n_intervals):
        
        if not selection:
            return dcc.Graph(
                figure=_placeholder_figure("Learn Chart", "Select a chart above to see a live example")
            )

        try:
            ticker = ticker or "AAPL"

            if selection == "candlestick":
                df = get_price_history(ticker, timeframe or "1m")
                return dcc.Graph(figure=price_chart(df), style={"height": "520px"})

            elif selection == "vol_smile":
                calls, puts = get_options_chain(ticker)
                fig = volatility_smile(calls, puts, get_stock_price(ticker))
                fig.update_layout(height=520)
                return dcc.Graph(figure=fig, style={"height": "520px"})

            elif selection == "options_chain":
                calls, _ = get_options_chain(ticker)
                if calls is None or calls.empty:
                    fig = _placeholder_figure("Options Chain", "Unable to load options chain")
                else:
                    spot = get_stock_price(ticker) or calls["strike"].median()
                    nearby = calls.copy()
                    nearby["distance"] = (nearby["strike"] - spot).abs()
                    nearby = nearby.nsmallest(20, "distance").sort_values("strike")
                    fig = options_chart(nearby)
                fig.update_layout(height=520)
                return dcc.Graph(figure=fig, style={"height": "520px"})

            elif selection == "oi":
                calls, puts = get_options_chain(ticker)
                fig = open_interest_chart(calls, puts, get_stock_price(ticker))
                fig.update_layout(height=580)
                return dcc.Graph(figure=fig, style={"height": "580px"})

            elif selection == "volume":
                calls, puts = get_options_chain(ticker)
                fig = volume_comparison(calls, puts)
                fig.update_layout(height=580)
                return dcc.Graph(figure=fig, style={"height": "580px"})

            elif selection == "returns":
                df = get_price_history(ticker, timeframe or "1m")
                fig = returns_chart(df)
                fig.update_layout(height=520)
                return dcc.Graph(figure=fig, style={"height": "520px"})

            elif selection == "pnl":
                fig = pnl_chart(pnl_strategy or "call", 100, 5)
                fig.update_layout(height=520)
                return dcc.Graph(figure=fig, style={"height": "520px"})

            elif selection == "greeks":
                S = get_stock_price(ticker)

                if S is None:
                    S = 100

                fig = greek_curve(S, S, 1, 0.05, 0.2, greek)
                fig.update_layout(height=520)
                return dcc.Graph(
                    figure=fig,
                    style={"height": "520px"}
                )

        except Exception as e:
            print("LEARN CHART ERROR:", e)
            return dcc.Graph(
                figure=_placeholder_figure("Learn Chart", "Chart unavailable")
            )


    @app.callback(
        Output("greek-container", "style"),
        Output("pnl-container", "style"),
        Input("learn-dropdown", "value")
    )
    def toggle_learn_controls(selection):
        if selection == "greeks":
            return {"display": "block", "marginBottom": "20px"}, {"display": "none"}
        if selection == "pnl":
            return {"display": "none"}, {"display": "block", "marginBottom": "20px"}
        return {"display": "none"}, {"display": "none"}

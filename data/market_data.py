import yfinance as yf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"].iloc[-1]

def get_price_history(ticker, timeframe="1m"):
    import yfinance as yf

    stock = yf.Ticker(ticker)

    interval_map = {
        "1m": ("1d", "1m"),
        "5m": ("5d", "5m"),
        "15m": ("1mo", "15m"),
        "1h": ("1mo", "1h"),
        "1d": ("6mo", "1d"),
    }

    period, interval = interval_map.get(timeframe, ("1d","1m"))

    df = stock.history(period=period, interval=interval)
    return df.dropna()

def get_options_chain(ticker):

    try:
        stock = yf.Ticker(ticker)
        expirations = stock.options

        if not expirations:
            print("No expirations")
            return None, None

        opt = stock.option_chain(expirations[0])

        return opt.calls, opt.puts

    except Exception as e:
        print("OPTIONS ERROR:", e)
        return None, None
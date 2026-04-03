import yfinance as yf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"].iloc[-1]

def get_options_chain(ticker):
    stock = yf.Ticker(ticker)
    expirations = stock.options

    if not expirations:
        return None, None

    opt = stock.option_chain(expirations[0])
    return opt.calls, opt.puts
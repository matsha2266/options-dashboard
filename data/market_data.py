import yfinance as yf
import time


_CACHE = {}


def _cache_get(key, ttl_seconds):
    entry = _CACHE.get(key)
    if not entry:
        return None
    if time.monotonic() - entry["ts"] > ttl_seconds:
        _CACHE.pop(key, None)
        return None
    return entry["value"]


def _cache_set(key, value):
    _CACHE[key] = {"ts": time.monotonic(), "value": value}


def _copy_df(df):
    return df.copy(deep=True) if df is not None else None

def get_stock_price(ticker):
    cache_key = ("stock_price", ticker)
    cached = _cache_get(cache_key, ttl_seconds=2)
    if cached is not None:
        return cached

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        if history.empty or "Close" not in history:
            return None
        price = history["Close"].iloc[-1]
        _cache_set(cache_key, price)
        return price
    except Exception:
        return None

def get_price_history(ticker, timeframe="1m"):
    cache_key = ("price_history", ticker, timeframe)
    cached = _cache_get(cache_key, ttl_seconds=2)
    if cached is not None:
        return _copy_df(cached)

    stock = yf.Ticker(ticker)

    interval_map = {
        "1m": ("1d", "1m"),
        "5m": ("5d", "5m"),
        "15m": ("1mo", "15m"),
        "1h": ("1mo", "1h"),
        "1d": ("6mo", "1d"),
    }

    period, interval = interval_map.get(timeframe, ("1d","1m"))

    try:
        df = stock.history(period=period, interval=interval)
        if df is None or df.empty:
            return df
        cleaned = df.dropna()
        _cache_set(cache_key, cleaned)
        return _copy_df(cleaned)
    except Exception:
        return None

def get_options_chain(ticker):
    cache_key = ("options_chain", ticker)
    cached = _cache_get(cache_key, ttl_seconds=15)
    if cached is not None:
        calls, puts = cached
        return _copy_df(calls), _copy_df(puts)

    try:
        stock = yf.Ticker(ticker)
        expirations = stock.options
        spot = get_stock_price(ticker)

        if not expirations:
            print("No expirations")
            return None, None

        best_calls = None
        best_puts = None
        best_score = -1

        for expiration in expirations[:40]:
            opt = stock.option_chain(expiration)
            calls = opt.calls
            puts = opt.puts

            if (calls is None or calls.empty) and (puts is None or puts.empty):
                continue

            if spot is not None and spot > 0:
                lower = spot * 0.8
                upper = spot * 1.2
                near_calls = calls[(calls["strike"] >= lower) & (calls["strike"] <= upper)] if calls is not None and "strike" in calls else None
                near_puts = puts[(puts["strike"] >= lower) & (puts["strike"] <= upper)] if puts is not None and "strike" in puts else None
            else:
                near_calls = calls
                near_puts = puts

            near_call_oi = int(near_calls["openInterest"].fillna(0).sum()) if near_calls is not None and "openInterest" in near_calls else 0
            near_put_oi = int(near_puts["openInterest"].fillna(0).sum()) if near_puts is not None and "openInterest" in near_puts else 0
            near_call_iv = int((near_calls["impliedVolatility"].fillna(0) > 0.02).sum()) if near_calls is not None and "impliedVolatility" in near_calls else 0
            near_put_iv = int((near_puts["impliedVolatility"].fillna(0) > 0.02).sum()) if near_puts is not None and "impliedVolatility" in near_puts else 0
            near_call_strikes = int(near_calls["strike"].notna().sum()) if near_calls is not None and "strike" in near_calls else 0
            near_put_strikes = int(near_puts["strike"].notna().sum()) if near_puts is not None and "strike" in near_puts else 0

            score = (
                (near_call_oi + near_put_oi) * 100
                + (near_call_iv + near_put_iv) * 250
                + (near_call_strikes + near_put_strikes) * 100
            )

            if score > best_score:
                best_score = score
                best_calls = calls
                best_puts = puts

        _cache_set(cache_key, (best_calls, best_puts))
        return _copy_df(best_calls), _copy_df(best_puts)

    except Exception as e:
        print("OPTIONS ERROR:", e)
        return None, None

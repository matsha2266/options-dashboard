import plotly.graph_objects as go
import numpy as np
from models.black_scholes import delta, gamma, vega

def greek_curve(S,K,T,r,sigma,greek):
    
    S_range = np.linspace(0.5*S, 1.5*S, 200)

    if greek == "Delta":
        values = [delta(s,K,T,r,sigma) for s in S_range]
    elif greek == "Gamma":
        values = [gamma(s,K,T,r,sigma) for s in S_range]
    elif greek == "Vega":
        values = [vega(s,K,T,r,sigma) for s in S_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=values, mode='lines'))

    fig.update_layout(
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=12,
            font_family="Arial"
        ),
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        title=f"{greek} Curve",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


def price_chart(df):

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        increasing_line_color="#00ff99",
        decreasing_line_color="#ff4d4d"
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        transition_duration=300,  
        uirevision=True  
    )

    return fig


def options_chart(calls):
    
    fig = go.Figure()
    fig.add_bar(x=calls["strike"], y=calls["lastPrice"])

    fig.update_layout(
        template="plotly_dark",
        title="Options Chain",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    return fig


def pnl_chart(strategy, strike, premium):
    import numpy as np
    import plotly.graph_objects as go

    S = np.linspace(50, 200, 100)

    if strategy == "call":
        pnl = np.maximum(S - strike, 0) - premium

    elif strategy == "put":
        pnl = np.maximum(strike - S, 0) - premium

    elif strategy == "bull_spread":
        pnl = np.maximum(S - strike, 0) - np.maximum(S - (strike + 10), 0) - premium

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=S,
        y=pnl,
        line=dict(color="#60a5fa", width=3)
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="white")

    fig.update_layout(
        template="plotly_dark",
        title="Strategy Payoff",
        xaxis_title="Stock Price",
        yaxis_title="Profit / Loss"
    )

    return fig




def volatility_smile(calls):
    import plotly.graph_objects as go

    if calls is None or calls.empty:
        return go.Figure()

    df = calls.dropna(subset=["strike", "impliedVolatility"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["strike"],
        y=df["impliedVolatility"],
        mode="lines+markers",
        line=dict(color="#60a5fa", width=2), 
        marker=dict(size=6),
        name="Implied Volatility"
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Volatility Smile",
        xaxis_title="Strike Price",
        yaxis_title="Implied Volatility",
        margin=dict(l=10, r=10, t=40, b=10)
    )

    return fig

def open_interest_chart(calls):
    import plotly.graph_objects as go

    if calls is None or calls.empty:
        return go.Figure()

    df = calls.dropna(subset=["strike", "openInterest"])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["strike"],
        y=df["openInterest"],
        marker_color="#f59e0b" 
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Open Interest by Strike",
        xaxis_title="Strike Price",
        yaxis_title="Open Interest",
        margin=dict(l=10, r=10, t=40, b=10)
    )

    return fig

def volume_comparison(calls, puts):
    import plotly.graph_objects as go

    if calls is None or puts is None:
        return go.Figure()

    call_vol = calls["volume"].sum()
    put_vol = puts["volume"].sum()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Calls", "Puts"],
        y=[call_vol, put_vol],
        marker_color=["#00ff99", "#ff4d4d"] 
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Call vs Put Volume",
        xaxis_title="Option Type",
        yaxis_title="Total Volume",
        margin=dict(l=10, r=10, t=40, b=10)
    )

    return fig


def returns_chart(df):
    import plotly.graph_objects as go

    df["returns"] = df["Close"].pct_change()

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df["returns"].dropna(),
        nbinsx=50,
        marker_color="#a78bfa" 
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Returns Distribution",
        xaxis_title="Returns",
        yaxis_title="Frequency",
        bargap=0.05
    )

    return fig
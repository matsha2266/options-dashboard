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
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines'))

    fig.update_layout(
        template="plotly_dark",
        title="Stock Price",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
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

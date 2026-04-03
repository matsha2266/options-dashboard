import plotly.graph_objects as go
import numpy as np
from models.black_scholes import delta, gamma, vega

def greek_curve(S,K,T,r,sigma,greek):
    S_range = np.linspace(0.5*S,1.5*S,200)

    if greek == "Delta":
        values = [delta(s,K,T,r,sigma) for s in S_range]
    elif greek == "Gamma":
        values = [gamma(s,K,T,r,sigma) for s in S_range]
    elif greek == "Vega":
        values = [vega(s,K,T,r,sigma) for s in S_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range,y=values,mode='lines'))

    fig.update_layout(
        template="plotly_dark",
        title=f"{greek} Curve",
        xaxis_title="Stock Price",
        yaxis_title=greek
    )
    return fig
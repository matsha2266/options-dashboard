import plotly.graph_objects as go
import numpy as np
import pandas as pd
from models.black_scholes import delta, gamma, vega, rho, theta


def _build_greek_grid(S, K, T, r, greek):
    if S is None or S <= 0:
        S = 100
    if K is None or K <= 0:
        K = S

    greek = (greek or "delta").lower()
    price_range = np.linspace(0.5 * S, 1.5 * S, 60)
    vol_range = np.linspace(0.05, 0.80, 50)

    z = []
    for vol in vol_range:
        row = []
        for price in price_range:
            if greek == "delta":
                val = delta(price, K, T, r, vol)
            elif greek == "gamma":
                val = gamma(price, K, T, r, vol)
            elif greek == "vega":
                val = vega(price, K, T, r, vol)
            elif greek == "theta":
                val = theta(price, K, T, r, vol)
            elif greek == "rho":
                val = rho(price, K, T, r, vol)
            else:
                val = 0
            row.append(val)
        z.append(row)

    return greek, price_range, vol_range, z

def greek_curve(S, K, T, r, sigma, greek):
    if S is None or S <= 0:
        S = 100
    if K is None or K <= 0:
        K = S

    greek = (greek or "delta").lower()

    S_range = np.linspace(0.5*S, 1.5*S, 200)

    if greek == "delta":
        values = [delta(s, K, T, r, sigma) for s in S_range]

    elif greek == "gamma":
        values = [gamma(s, K, T, r, sigma) for s in S_range]

    elif greek == "vega":
        values = [vega(s, K, T, r, sigma) for s in S_range]

    elif greek == "theta":
        values = [theta(s, K, T, r, sigma) for s in S_range]

    elif greek == "rho":
        values = [rho(s, K, T, r, sigma) for s in S_range]

    else:
        values = [0 for _ in S_range]

    color_map = {
        "delta": "#00FFAA",
        "gamma": "#FF4D4D",
        "vega": "#60A5FA",
        "theta": "#FBBF24",
        "rho": "#C084FC"
    }

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=S_range,
        y=values,
        mode='lines',
        line=dict(width=3, color=color_map.get(greek, "white")),
        name=greek.capitalize()
    ))

    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        font=dict(color="white"),
        title=f"{greek.capitalize()} vs Price",
        xaxis_title="Underlying Price",
        yaxis_title=greek.capitalize(),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


def greek_heatmap(S, K, T, r, sigma, greek, colorscale="RdYlGn"):
    greek, price_range, vol_range, z = _build_greek_grid(S, K, T, r, greek)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=price_range,
        y=vol_range,
        colorscale=colorscale,
        colorbar=dict(
            title=dict(
                text=greek.capitalize(),
                side="right",
                font=dict(size=10)
            ),
            tickfont=dict(size=9),
            thickness=10
        ),
        hovertemplate="Price: %{x:.2f}<br>Vol: %{y:.2f}<br>" + greek.capitalize() + ": %{z:.4f}<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text=f"{greek.capitalize()} Heatmap", font=dict(size=12)),
        xaxis_title="Price",
        yaxis_title="Vol",
        margin=dict(l=10, r=10, t=32, b=10),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="white", size=10),
        xaxis=dict(tickfont=dict(size=9), title_font=dict(size=10)),
        yaxis=dict(tickfont=dict(size=9), title_font=dict(size=10))
    )

    return fig


def greek_surface(S, K, T, r, sigma, greek, colorscale="Earth"):
    greek, price_range, vol_range, z = _build_greek_grid(S, K, T, r, greek)
    z_array = np.array(z)
    z_min = float(z_array.min())
    z_max = float(z_array.max())
    z_mid = float((z_min + z_max) / 2)
    contour_step = (z_max - z_min) / 12 if z_max != z_min else 1

    fig = go.Figure(data=go.Surface(
        z=z,
        x=price_range,
        y=vol_range,
        colorscale=colorscale,
        colorbar=dict(
            title=dict(
                text=greek.capitalize(),
                font=dict(size=11)
            ),
            tickfont=dict(size=10),
            thickness=12
        ),
        contours={
            "x": {
                "show": True,
                "color": "rgba(255,255,255,0.22)",
                "highlight": False,
                "start": float(price_range.min()),
                "end": float(price_range.max()),
                "size": float((price_range.max() - price_range.min()) / 10)
            },
            "y": {
                "show": True,
                "color": "rgba(255,255,255,0.18)",
                "highlight": False,
                "start": float(vol_range.min()),
                "end": float(vol_range.max()),
                "size": float((vol_range.max() - vol_range.min()) / 8)
            },
            "z": {
                "show": True,
                "usecolormap": True,
                "highlightcolor": "limegreen",
                "project": {"z": True},
                "start": z_min,
                "end": z_max,
                "size": contour_step
            }
        },
        lighting={
            "ambient": 0.35,
            "diffuse": 0.95,
            "roughness": 0.95,
            "specular": 0.03,
            "fresnel": 0.02
        },
        lightposition={"x": 150, "y": 90, "z": 240},
        hovertemplate="Price: %{x:.2f}<br>Vol: %{y:.2f}<br>" + greek.capitalize() + ": %{z:.4f}<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text=f"{greek.capitalize()} Surface", font=dict(size=18)),
        autosize=False,
        scene=dict(
            xaxis_title="Underlying Price",
            yaxis_title="Volatility",
            zaxis_title=greek.capitalize(),
            xaxis=dict(backgroundcolor="#111827", gridcolor="#334155", zerolinecolor="#334155"),
            yaxis=dict(backgroundcolor="#111827", gridcolor="#334155", zerolinecolor="#334155"),
            zaxis=dict(
                backgroundcolor="#111827",
                gridcolor="#334155",
                zerolinecolor="#334155",
                tickfont=dict(size=10),
                range=[z_min, z_max] if z_max != z_min else None
            ),
            aspectratio=dict(x=1, y=1, z=0.55),
            camera=dict(
                eye=dict(x=1.55, y=1.55, z=0.9),
                center=dict(x=0, y=0, z=0),
                up=dict(x=0, y=0, z=1)
            )
        ),
        paper_bgcolor="#111827",
        margin=dict(l=0, r=0, t=44, b=0),
        font=dict(color="white"),
        annotations=[dict(
            text=f"Topographic relief centered near {z_mid:.4f}",
            x=0,
            y=1.02,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=11, color="#94a3b8")
        )]
    )

    return fig


def price_chart(df):
    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            title="Price Chart Unavailable",
            annotations=[{
                "text": "No price data available",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"color": "white"}
            }]
        )
        return fig

    chart_df = df.copy()
    chart_df["ma_fast"] = chart_df["Close"].rolling(window=9, min_periods=1).mean()
    chart_df["ma_slow"] = chart_df["Close"].rolling(window=21, min_periods=1).mean()

    completed_df = chart_df.iloc[:-1]
    last_close = float(chart_df["Close"].iloc[-1])
    last_open = float(chart_df["Open"].iloc[-1])
    last_high = float(chart_df["High"].iloc[-1])
    last_low = float(chart_df["Low"].iloc[-1])
    live_x = chart_df.index[-1]
    live_color = "#00ff99" if last_close >= last_open else "#ff4d4d"

    scale_df = completed_df if not completed_df.empty else chart_df
    y_min = float(scale_df["Low"].min())
    y_max = float(scale_df["High"].max())
    y_min = min(y_min, last_low, last_open, last_close)
    y_max = max(y_max, last_high, last_open, last_close)
    y_span = max(y_max - y_min, max(last_close * 0.002, 0.05))
    y_pad = max(y_span * 0.04, max(last_close * 0.002, 0.05))

    if len(chart_df.index) > 1:
        candle_step = chart_df.index[-1] - chart_df.index[-2]
    else:
        candle_step = pd.Timedelta(minutes=1)
    body_half_width = candle_step * 0.32
    min_body = max(y_span * 0.01, max(last_close * 0.0008, 0.02))
    body_delta = last_close - last_open
    if abs(body_delta) < min_body:
        body_delta = min_body if body_delta >= 0 else -min_body
    body_top = last_open + body_delta

    x_start = chart_df.index[0]
    if not completed_df.empty:
        x_end_anchor = completed_df.index[-1]
        x_start_anchor = completed_df.index[0]
        x_start = x_start_anchor - (candle_step * 0.5)
        x_end = x_end_anchor + (candle_step * 1.5)
    else:
        x_start = live_x - (candle_step * 20)
        x_end = live_x + (candle_step * 1.5)

    fig = go.Figure()

    if not completed_df.empty:
        fig.add_trace(go.Candlestick(
            x=completed_df.index,
            open=completed_df["Open"],
            high=completed_df["High"],
            low=completed_df["Low"],
            close=completed_df["Close"],
            increasing_line_color="#00ff99",
            decreasing_line_color="#ff4d4d",
            increasing_fillcolor="rgba(0, 255, 153, 0.55)",
            decreasing_fillcolor="rgba(255, 77, 77, 0.55)",
            name="Candles"
        ))

    fig.add_trace(go.Scatter(
        x=[live_x, live_x],
        y=[last_low, last_high],
        mode="lines",
        line=dict(color=live_color, width=2),
        name="Live Wick",
        hoverinfo="skip",
        showlegend=False
    ))

    fig.add_trace(go.Bar(
        x=[live_x],
        y=[body_delta],
        base=[last_open],
        width=[int(candle_step.total_seconds() * 1000 * 0.64)],
        marker=dict(
            color="rgba(0, 255, 153, 0.6)" if live_color == "#00ff99" else "rgba(255, 77, 77, 0.6)",
            line=dict(color=live_color, width=2)
        ),
        name="Live Candle",
        hovertemplate=(
            f"Open: {last_open:.2f}<br>"
            f"High: {last_high:.2f}<br>"
            f"Low: {last_low:.2f}<br>"
            f"Close: {last_close:.2f}<extra></extra>"
        )
    ))

    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df["ma_fast"],
        mode="lines",
        line=dict(color="#f59e0b", width=2),
        name="MA 9"
    ))

    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df["ma_slow"],
        mode="lines",
        line=dict(color="#60a5fa", width=2),
        name="MA 21"
    ))

    fig.add_hline(
        y=last_close,
        line_dash="dot",
        line_color=live_color,
        opacity=0.7
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        transition_duration=0,
        uirevision=False,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(range=[y_min - y_pad, y_max + y_pad]),
        xaxis=dict(range=[x_start, x_end])
    )

    return fig


def options_chart(calls):
    if calls is None or calls.empty:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", title="Options Chain Unavailable")
        return fig
    
    fig = go.Figure()
    fig.add_bar(x=calls["strike"], y=calls["lastPrice"])

    fig.update_layout(
        template="plotly_dark",
        title="Options Chain"
    )

    return fig


def pnl_chart(option_type, K, premium):
    if K is None or K <= 0:
        K = 100
    if premium is None:
        premium = 0

    S_range = np.linspace(0.5*K, 1.5*K, 200)
    spread_width = max(5, round(K * 0.1))
    outer_width = max(5, round(K * 0.08))

    option_type = option_type or "call"

    if option_type == "call":
        pnl = [max(s - K, 0) - premium for s in S_range]

    elif option_type == "put":
        pnl = [max(K - s, 0) - premium for s in S_range]

    elif option_type == "short_call":
        pnl = [premium - max(s - K, 0) for s in S_range]

    elif option_type == "short_put":
        pnl = [premium - max(K - s, 0) for s in S_range]

    elif option_type == "bull_call_spread":
        long_strike = K
        short_strike = K + spread_width
        net_debit = premium
        pnl = [
            max(s - long_strike, 0) - max(s - short_strike, 0) - net_debit
            for s in S_range
        ]

    elif option_type == "bear_put_spread":
        long_strike = K
        short_strike = K - spread_width
        net_debit = premium
        pnl = [
            max(long_strike - s, 0) - max(short_strike - s, 0) - net_debit
            for s in S_range
        ]

    elif option_type == "long_straddle":
        total_premium = premium * 2
        pnl = [
            max(s - K, 0) + max(K - s, 0) - total_premium
            for s in S_range
        ]

    elif option_type == "long_strangle":
        put_strike = K - outer_width
        call_strike = K + outer_width
        total_premium = premium * 2
        pnl = [
            max(s - call_strike, 0) + max(put_strike - s, 0) - total_premium
            for s in S_range
        ]

    else:
        pnl = [0 for _ in S_range]

    title_map = {
        "call": "Long Call PnL",
        "put": "Long Put PnL",
        "short_call": "Short Call PnL",
        "short_put": "Short Put PnL",
        "bull_call_spread": "Bull Call Spread PnL",
        "bear_put_spread": "Bear Put Spread PnL",
        "long_straddle": "Long Straddle PnL",
        "long_strangle": "Long Strangle PnL",
    }

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=S_range,
        y=pnl,
        mode="lines",
        line=dict(color="#00FFAA", width=3)
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="white")

    fig.update_layout(
        template="plotly_dark",
        title=title_map.get(option_type, "PnL at Expiration"),
        xaxis_title="Underlying Price",
        yaxis_title="Profit / Loss"
    )

    return fig



def _option_window(df, spot=None, width=0.22, max_points=24):
    if df is None or df.empty or "strike" not in df:
        return df

    cleaned = df.sort_values("strike").copy()
    if spot is None or spot <= 0:
        midpoint = cleaned["strike"].median()
    else:
        midpoint = spot

    if midpoint and midpoint > 0:
        lower = midpoint * (1 - width)
        upper = midpoint * (1 + width)
        window = cleaned[(cleaned["strike"] >= lower) & (cleaned["strike"] <= upper)].copy()
        if not window.empty:
            cleaned = window

    if len(cleaned) > max_points:
        cleaned = cleaned.assign(distance=(cleaned["strike"] - midpoint).abs())
        cleaned = cleaned.nsmallest(max_points, "distance").sort_values("strike")

    return cleaned.drop(columns=["distance"], errors="ignore")


def volatility_smile(calls, puts=None, spot=None):
    import plotly.graph_objects as go

    datasets = []
    if calls is not None and not calls.empty:
        call_df = calls.dropna(subset=["strike", "impliedVolatility"]).copy()
        datasets.append(call_df[["strike", "impliedVolatility"]])
    if puts is not None and not puts.empty:
        put_df = puts.dropna(subset=["strike", "impliedVolatility"]).copy()
        datasets.append(put_df[["strike", "impliedVolatility"]])

    if not datasets:
        return go.Figure()

    df = pd.concat(datasets, ignore_index=True)
    df = (
        df.groupby("strike", as_index=False)["impliedVolatility"]
        .mean()
        .sort_values("strike")
    )
    df = _option_window(df, spot=spot, width=0.18, max_points=22)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["strike"],
        y=df["impliedVolatility"],
        mode="lines+markers",
        line=dict(color="#60a5fa", width=3, shape="spline", smoothing=0.7),
        marker=dict(size=6, color="#93c5fd"),
        name="Implied Volatility"
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text="Volatility Smile", pad=dict(t=18)),
        xaxis_title="Strike Price",
        yaxis_title="Implied Volatility",
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False
    )

    return fig

def open_interest_chart(calls, puts=None, spot=None):
    import plotly.graph_objects as go

    raw_call_df = None
    raw_put_df = None
    call_df = None
    put_df = None
    if calls is not None and not calls.empty:
        raw_call_df = calls.dropna(subset=["strike", "openInterest"])[["strike", "openInterest"]].copy()
        call_df = raw_call_df.copy()
    if puts is not None and not puts.empty:
        raw_put_df = puts.dropna(subset=["strike", "openInterest"])[["strike", "openInterest"]].copy()
        put_df = raw_put_df.copy()

    if call_df is None and put_df is None:
        return go.Figure()

    if spot is not None and spot > 0:
        if call_df is not None and not call_df.empty:
            call_df = _option_window(call_df, spot=spot, width=0.18, max_points=18)
        if put_df is not None and not put_df.empty:
            put_df = _option_window(put_df, spot=spot, width=0.18, max_points=18)

    combined = pd.concat(
        [df for df in [call_df, put_df] if df is not None and not df.empty],
        ignore_index=True
    ) if any(df is not None and not df.empty for df in [call_df, put_df]) else pd.DataFrame()

    raw_combined = pd.concat(
        [df for df in [raw_call_df, raw_put_df] if df is not None and not df.empty],
        ignore_index=True
    ) if any(df is not None and not df.empty for df in [raw_call_df, raw_put_df]) else pd.DataFrame()

    if combined.empty and raw_combined.empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            title="Open Interest by Strike",
            annotations=[{
                "text": "No meaningful open interest in this chain",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"color": "white"}
            }]
        )
        return fig

    source_strikes = raw_combined if not raw_combined.empty else combined
    all_strikes = sorted(source_strikes["strike"].unique())

    if raw_call_df is not None and not raw_call_df.empty:
        full_call_series = raw_call_df.groupby("strike")["openInterest"].sum().reindex(all_strikes, fill_value=0)
    else:
        full_call_series = pd.Series(0, index=all_strikes)

    if raw_put_df is not None and not raw_put_df.empty:
        full_put_series = raw_put_df.groupby("strike")["openInterest"].sum().reindex(all_strikes, fill_value=0)
    else:
        full_put_series = pd.Series(0, index=all_strikes)

    nonzero_strikes = [
        strike for strike in all_strikes
        if full_call_series.loc[strike] > 0 or full_put_series.loc[strike] > 0
    ]

    if nonzero_strikes:
        selected = set(nonzero_strikes)
        remaining = max(0, 18 - len(selected))
        if remaining > 0:
            midpoint = spot if spot is not None and spot > 0 else np.median(all_strikes)
            nearby = [strike for strike in sorted(all_strikes, key=lambda strike: abs(strike - midpoint)) if strike not in selected]
            selected.update(nearby[:remaining])
        all_strikes = sorted(selected)
    elif len(all_strikes) > 18:
        midpoint = spot if spot is not None and spot > 0 else np.median(all_strikes)
        all_strikes = sorted(sorted(all_strikes, key=lambda strike: abs(strike - midpoint))[:18])

    call_series = full_call_series.reindex(all_strikes, fill_value=0)
    put_series = full_put_series.reindex(all_strikes, fill_value=0)
    strike_positions = list(range(len(all_strikes)))
    strike_labels = [
        str(int(strike)) if float(strike).is_integer() else f"{strike:.1f}"
        for strike in all_strikes
    ]
    tick_step = 1 if len(strike_positions) <= 10 else 2
    tick_positions = strike_positions[::tick_step]
    tick_labels = strike_labels[::tick_step]

    max_oi = max(call_series.max() if len(call_series) else 0, put_series.max() if len(put_series) else 0)
    top_call_strike = call_series.idxmax() if len(call_series) and call_series.max() > 0 else None
    top_put_strike = put_series.idxmax() if len(put_series) and put_series.max() > 0 else None

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=strike_positions,
        y=call_series.tolist(),
        marker_color="#ef4444",
        marker_line_color="#fca5a5",
        marker_line_width=1,
        name="Calls OI",
        offsetgroup="calls",
        hovertemplate="Strike %{x}<br>Calls OI %{y:,}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=strike_positions,
        y=put_series.tolist(),
        marker_color="#22c55e",
        marker_line_color="#86efac",
        marker_line_width=1,
        name="Puts OI",
        offsetgroup="puts",
        hovertemplate="Strike %{x}<br>Puts OI %{y:,}<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text="Open Interest by Strike", pad=dict(t=18)),
        xaxis_title="Strike Price",
        yaxis_title="Open Interest",
        margin=dict(l=10, r=10, t=40, b=10),
        barmode="group",
        bargap=0.18,
        bargroupgap=0.08,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    if max_oi > 0:
        fig.update_yaxes(
            range=[0, max_oi * 1.2],
            gridcolor="#1f2937",
            zeroline=False
        )
    fig.update_xaxes(
        type="linear",
        tickmode="array",
        tickvals=tick_positions,
        ticktext=tick_labels,
        range=[-0.6, len(strike_positions) - 0.4] if strike_positions else None,
        tickangle=-25,
        gridcolor="#1f2937",
        tickfont=dict(size=9)
    )

    if spot is not None and spot > 0:
        nearest_strike = min(all_strikes, key=lambda strike: abs(strike - spot))
        nearest_index = all_strikes.index(nearest_strike)
        fig.add_vline(
            x=nearest_index,
            line_width=2,
            line_dash="dash",
            line_color="#eab308",
            opacity=0.85
        )
        fig.add_annotation(
            x=nearest_index,
            y=max_oi * 1.14 if max_oi > 0 else 1,
            text=f"Spot ~ {spot:.2f}",
            showarrow=False,
            font=dict(size=11, color="#fde68a"),
            bgcolor="rgba(15,23,42,0.9)",
            bordercolor="#eab308",
            borderwidth=1
        )

    if top_call_strike is not None:
        fig.add_annotation(
            x=top_call_strike,
            y=call_series.loc[top_call_strike],
            text="Max Call OI",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=10, color="#fecaca"),
            arrowcolor="#ef4444"
        )
    if top_put_strike is not None:
        fig.add_annotation(
            x=top_put_strike,
            y=put_series.loc[top_put_strike],
            text="Max Put OI",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=10, color="#bbf7d0"),
            arrowcolor="#22c55e"
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
        title=dict(text="Call vs Put Volume", pad=dict(t=18)),
        xaxis_title="Option Type",
        yaxis_title="Total Volume",
        margin=dict(l=10, r=10, t=40, b=10)
    )

    return fig


def returns_chart(df):
    import plotly.graph_objects as go

    if df is None or df.empty or "Close" not in df:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", title="Returns Unavailable")
        return fig

    df = df.copy()
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

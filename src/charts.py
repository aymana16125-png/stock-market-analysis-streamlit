from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def create_price_figure(df: pd.DataFrame, symbol: str):
    """Create a stock closing price chart with moving averages."""
    fig = go.Figure()

    if df is None or df.empty:
        fig.update_layout(
            title=f"No chart available for {symbol.upper()}",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Price",
        )
        return fig

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close",
        )
    )

    if "MA_5" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["MA_5"],
                mode="lines",
                name="MA 5",
            )
        )

    if "MA_10" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["MA_10"],
                mode="lines",
                name="MA 10",
            )
        )

    fig.update_layout(
        title=f"{symbol.upper()} Price Trend",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        hovermode="x unified",
        legend_title_text="Series",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig

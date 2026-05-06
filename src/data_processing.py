from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def clean_history(history: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of yfinance historical data."""
    if history is None or history.empty:
        return pd.DataFrame(columns=["Date", *REQUIRED_COLUMNS])

    df = history.copy()
    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()
    elif "Date" not in df.columns:
        df = df.reset_index()

    if "Date" not in df.columns:
        if "index" in df.columns:
            df = df.rename(columns={"index": "Date"})
        elif "Datetime" in df.columns:
            df = df.rename(columns={"Datetime": "Date"})

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    keep_columns = [c for c in ["Date", *REQUIRED_COLUMNS] if c in df.columns]
    df = df[keep_columns].copy()
    df = df.dropna(subset=["Date", "Close"], how="any")
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.sort_values("Date")
    return df.reset_index(drop=True)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add basic indicators for visualization and analysis."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["Date", *REQUIRED_COLUMNS, "Daily Change", "Daily Return %", "MA_5", "MA_10"])

    out = df.copy()
    out["Daily Change"] = out["Close"].diff()
    out["Daily Return %"] = out["Close"].pct_change() * 100
    out["MA_5"] = out["Close"].rolling(window=5, min_periods=1).mean()
    out["MA_10"] = out["Close"].rolling(window=10, min_periods=1).mean()
    return out


def summarize_history(df: pd.DataFrame) -> dict[str, float | int | None]:
    if df is None or df.empty:
        return {
            "rows": 0,
            "latest_close": None,
            "highest_high": None,
            "lowest_low": None,
            "average_volume": None,
        }

    return {
        "rows": int(len(df)),
        "latest_close": float(df["Close"].iloc[-1]),
        "highest_high": float(df["High"].max()) if "High" in df.columns else None,
        "lowest_low": float(df["Low"].min()) if "Low" in df.columns else None,
        "average_volume": int(df["Volume"].mean()) if "Volume" in df.columns and not df["Volume"].isna().all() else None,
    }

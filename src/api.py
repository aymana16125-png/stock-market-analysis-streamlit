from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import pandas as pd
try:
    import yfinance as yf
except ImportError:  # pragma: no cover - fallback for environments without yfinance
    class _YFinanceFallback:
        def Ticker(self, *args, **kwargs):
            raise ImportError("yfinance is required to fetch stock data.")

    yf = _YFinanceFallback()


@dataclass
class StockPayload:
    symbol: str
    name: str
    current_price: Optional[float]
    currency: Optional[str]
    history: pd.DataFrame
    market_cap: Optional[float]
    volume: Optional[int]
    error: Optional[str] = None


def _normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def _extract_info(info: dict[str, Any], symbol: str) -> dict[str, Any]:
    name = (
        info.get("shortName")
        or info.get("longName")
        or info.get("displayName")
        or symbol
    )
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    currency = info.get("currency")
    market_cap = info.get("marketCap")
    volume = info.get("volume") or info.get("regularMarketVolume")
    return {
        "name": name,
        "current_price": current_price,
        "currency": currency,
        "market_cap": market_cap,
        "volume": volume,
    }


def fetch_stock_data(symbol: str, period: str = "1mo", interval: str = "1d") -> StockPayload:
    """Fetch current and historical data for a stock symbol.

    Returns a StockPayload object with either data or an error message.
    """
    symbol = _normalize_symbol(symbol)
    if not symbol:
        return StockPayload(
            symbol="",
            name="",
            current_price=None,
            currency=None,
            history=pd.DataFrame(),
            market_cap=None,
            volume=None,
            error="Please enter a stock symbol.",
        )

    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval, auto_adjust=False)
        if history is None or history.empty:
            return StockPayload(
                symbol=symbol,
                name=symbol,
                current_price=None,
                currency=None,
                history=pd.DataFrame(),
                market_cap=None,
                volume=None,
                error=f"No historical data found for {symbol}.",
            )

        info: dict[str, Any] = {}
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        extracted = _extract_info(info, symbol)
        if extracted["current_price"] is None:
            extracted["current_price"] = float(history["Close"].iloc[-1])

        return StockPayload(
            symbol=symbol,
            name=extracted["name"],
            current_price=float(extracted["current_price"])
            if extracted["current_price"] is not None
            else None,
            currency=extracted["currency"],
            history=history,
            market_cap=extracted["market_cap"],
            volume=extracted["volume"],
            error=None,
        )
    except Exception as exc:
        return StockPayload(
            symbol=symbol,
            name=symbol,
            current_price=None,
            currency=None,
            history=pd.DataFrame(),
            market_cap=None,
            volume=None,
            error=f"Failed to fetch data for {symbol}: {exc}",
        )

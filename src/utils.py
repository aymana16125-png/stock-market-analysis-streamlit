from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT_DIR / "data" / "stock_catalog.csv"

DEFAULT_CATALOG = pd.DataFrame(
    [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc. Class A"},
        {"symbol": "AMZN", "name": "Amazon.com, Inc."},
        {"symbol": "TSLA", "name": "Tesla, Inc."},
    ]
)


def format_currency(value, currency: str | None = "USD") -> str:
    if value is None or pd.isna(value):
        return "N/A"
    currency = currency or "USD"
    return f"{currency} {value:,.2f}"


def format_number(value) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def validate_symbol(symbol: str) -> tuple[bool, str]:
    symbol = (symbol or "").strip()
    if not symbol:
        return False, "Stock symbol cannot be empty."
    if len(symbol) > 15:
        return False, "Stock symbol looks too long."
    if not symbol.replace(".", "").replace("-", "").isalnum():
        return False, "Stock symbol contains invalid characters."
    return True, ""


def _normalize_catalog(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=["symbol", "name", "display"])

    out = df.copy()
    out["symbol"] = out["symbol"].astype(str).str.strip().str.upper()
    out["name"] = out["name"].astype(str).str.strip()
    out = out.dropna(subset=["symbol", "name"])
    out = out[out["symbol"] != ""]
    out = out[out["name"] != ""]
    out = out.drop_duplicates(subset=["symbol"], keep="first").sort_values(["symbol", "name"])
    out["display"] = out["symbol"] + " | " + out["name"]
    return out.reset_index(drop=True)


@lru_cache(maxsize=1)
def load_stock_catalog() -> pd.DataFrame:
    if CATALOG_PATH.exists():
        try:
            df = pd.read_csv(CATALOG_PATH)
        except Exception:
            df = DEFAULT_CATALOG.copy()
    else:
        df = DEFAULT_CATALOG.copy()

    return _normalize_catalog(df)


def search_stock_catalog(query: str, limit: int = 30) -> pd.DataFrame:
    catalog = load_stock_catalog()
    if catalog.empty:
        return catalog

    query = (query or "").strip().lower()
    if not query:
        return catalog.head(limit).reset_index(drop=True)

    mask = catalog["symbol"].str.lower().str.contains(query, na=False) | catalog["name"].str.lower().str.contains(query, na=False)
    results = catalog.loc[mask].copy()

    if results.empty:
        return results

    symbol_exact = results["symbol"].str.lower().eq(query)
    name_exact = results["name"].str.lower().eq(query)
    prefix_match = results["symbol"].str.lower().str.startswith(query) | results["name"].str.lower().str.startswith(query)

    results["rank"] = 3
    results.loc[prefix_match, "rank"] = 2
    results.loc[symbol_exact | name_exact, "rank"] = 1
    results = results.sort_values(["rank", "symbol", "name"]).drop(columns=["rank"]).head(limit)
    return results.reset_index(drop=True)


def display_to_symbol(display_value: str) -> str:
    value = (display_value or "").strip()
    if " | " in value:
        return value.split(" | ", 1)[0].strip().upper()
    return value.upper()

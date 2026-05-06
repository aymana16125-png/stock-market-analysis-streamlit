from __future__ import annotations

import pandas as pd


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
    if len(symbol) > 10:
        return False, "Stock symbol looks too long."
    if not symbol.replace(".", "").replace("-", "").isalnum():
        return False, "Stock symbol contains invalid characters."
    return True, ""

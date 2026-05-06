import pandas as pd

from src.utils import display_to_symbol, load_stock_catalog, search_stock_catalog, validate_symbol


def test_display_to_symbol_parses_symbol_prefix():
    assert display_to_symbol("AAPL | Apple Inc.") == "AAPL"


def test_load_stock_catalog_has_display_column():
    catalog = load_stock_catalog()
    assert not catalog.empty
    assert {"symbol", "name", "display"}.issubset(catalog.columns)


def test_search_stock_catalog_filters_by_name():
    results = search_stock_catalog("apple")
    assert not results.empty
    assert "AAPL" in results["symbol"].tolist()


def test_validate_symbol_rejects_invalid_characters():
    ok, msg = validate_symbol("AAPL!!!")
    assert ok is False
    assert "invalid" in msg.lower()

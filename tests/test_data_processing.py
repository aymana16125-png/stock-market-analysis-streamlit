import pandas as pd

from src.data_processing import add_indicators, clean_history, summarize_history
from src.utils import validate_symbol


def test_validate_symbol_accepts_valid_symbol():
    ok, msg = validate_symbol("AAPL")
    assert ok is True
    assert msg == ""


def test_validate_symbol_rejects_blank():
    ok, msg = validate_symbol("   ")
    assert ok is False
    assert "empty" in msg.lower()


def test_clean_history_returns_sorted_dates():
    df = pd.DataFrame(
        {
            "Open": [2, 1],
            "High": [3, 2],
            "Low": [1, 0.5],
            "Close": [2.5, 1.5],
            "Volume": [200, 100],
        },
        index=pd.to_datetime(["2025-01-02", "2025-01-01"]),
    )
    cleaned = clean_history(df)
    assert list(cleaned["Date"].astype(str)) == ["2025-01-01", "2025-01-02"]
    assert list(cleaned.columns) == ["Date", "Open", "High", "Low", "Close", "Volume"]


def test_add_indicators_creates_expected_columns():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]).date,
            "Open": [1, 2, 3],
            "High": [2, 3, 4],
            "Low": [0.5, 1.5, 2.5],
            "Close": [1.5, 2.5, 3.5],
            "Volume": [100, 200, 300],
        }
    )
    enriched = add_indicators(df)
    for column in ["Daily Change", "Daily Return %", "MA_5", "MA_10"]:
        assert column in enriched.columns


def test_summarize_history_works():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2025-01-01", "2025-01-02"]).date,
            "Open": [1, 2],
            "High": [2, 3],
            "Low": [0.5, 1.5],
            "Close": [1.5, 2.5],
            "Volume": [100, 200],
        }
    )
    summary = summarize_history(df)
    assert summary["rows"] == 2
    assert summary["latest_close"] == 2.5

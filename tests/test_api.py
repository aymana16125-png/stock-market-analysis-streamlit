from unittest.mock import MagicMock, patch

import pandas as pd

from src.api import fetch_stock_data


@patch("src.api.yf.Ticker")
def test_fetch_stock_data_uses_mock_ticker(mock_ticker_cls):
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame(
        {
            "Open": [1.0, 2.0],
            "High": [1.5, 2.5],
            "Low": [0.8, 1.9],
            "Close": [1.2, 2.2],
            "Volume": [100, 200],
        },
        index=pd.to_datetime(["2025-01-01", "2025-01-02"]),
    )
    mock_ticker.info = {
        "shortName": "Test Corp",
        "currentPrice": 2.2,
        "currency": "USD",
        "marketCap": 123456,
        "volume": 200,
    }
    mock_ticker_cls.return_value = mock_ticker

    payload = fetch_stock_data("TEST")
    assert payload.error is None
    assert payload.name == "Test Corp"
    assert payload.current_price == 2.2
    assert not payload.history.empty

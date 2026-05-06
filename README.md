# Stock Market Analysis System

A simple Streamlit application that searches stock symbols, fetches current and historical prices from Yahoo Finance, and displays charts and summary statistics.

## Features
- Search stock symbols
- Display current price and stock details
- Display historical data
- Show trend charts
- Handle invalid input
- Basic testing with pytest

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- yfinance

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Testing
```bash
python -m pytest -q
```

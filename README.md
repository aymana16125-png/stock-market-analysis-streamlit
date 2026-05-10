# Stock Market Analysis System

A simple Streamlit application that searches stock symbols, offers live symbol-name suggestions, fetches current and historical prices from Yahoo Finance, and displays charts and summary statistics.

## Features
- Search stock symbols
- Display current price and stock details
- Display historical data
- Show trend charts
- Handle invalid input
- Live searchable stock suggestions
- Manual symbol entry remains available by default
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
pytest -q
```

## GitHub Workflow
- Create `main` and `dev` branches
- Each member works on a feature branch
- Open pull requests into `dev`
- Merge `dev` into `main` when complete

## Suggested Team Split
See `docs/task-board.md`.

## Diagram Files
Mermaid versions of the required diagrams are in `docs/diagrams/`.

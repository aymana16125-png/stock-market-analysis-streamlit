from __future__ import annotations

import streamlit as st

from src.api import fetch_stock_data
from src.charts import create_price_figure
from src.data_processing import add_indicators, clean_history, summarize_history
from src.utils import (
    display_to_symbol,
    format_currency,
    format_number,
    load_stock_catalog,
    search_stock_catalog,
    validate_symbol,
)


st.set_page_config(
    page_title="Stock Market Analysis System",
    page_icon="📈",
    layout="wide",
)

if "manual_symbol" not in st.session_state:
    st.session_state.manual_symbol = "AAPL"

if "auto_load" not in st.session_state:
    st.session_state.auto_load = True


def apply_selected_suggestion(selected_display: str) -> None:
    symbol = display_to_symbol(selected_display)
    if symbol:
        st.session_state.manual_symbol = symbol
        st.session_state.auto_load = True


st.title("Stock Market Analysis System")
st.caption(
    "Streamlit app for searching stocks, displaying current prices, and plotting historical trends."
)

catalog = load_stock_catalog()

with st.sidebar:
    st.header("Controls")
    st.text_input(
        "Stock Symbol",
        key="manual_symbol",
        help="Default entry. You can still type any valid ticker manually.",
    )
    period = st.selectbox("Historical Period", ["7d", "1mo", "3mo", "6mo", "1y"], index=1)
    interval_map = {
        "7d": "1d",
        "1mo": "1d",
        "3mo": "1d",
        "6mo": "1d",
        "1y": "1d",
    }
    interval = interval_map[period]

    st.divider()
    st.subheader("Live Stock Suggestions")
    search_query = st.text_input(
        "Search by symbol or company name",
        value="",
        help="Type part of a symbol or company name to filter the list.",
        placeholder="Example: Apple, Tesla, JPM, NVIDIA",
    )
    suggestions = search_stock_catalog(search_query, limit=25)

    if suggestions.empty:
        st.info("No matching symbols found. Use the manual symbol input above.")
        selected_display = None
        apply_disabled = True
    else:
        selected_display = st.selectbox(
            "Suggested symbols",
            suggestions["display"].tolist(),
            index=0,
            help="Select a symbol-name pair from the filtered list.",
        )
        st.caption(f"{len(suggestions)} match(es) shown")
        apply_disabled = False

    apply_suggestion = st.button(
        "Use selected suggestion",
        type="secondary",
        disabled=apply_disabled,
        help="Copy the selected symbol into the manual field and reload the data.",
    )

    load_button = st.button("Load Data", type="primary")

if apply_suggestion and selected_display:
    apply_selected_suggestion(selected_display)
    st.rerun()

symbol = (st.session_state.manual_symbol or "").strip().upper()
should_load = load_button or st.session_state.auto_load or "loaded_once" not in st.session_state

if should_load:
    st.session_state.loaded_once = True
    st.session_state.auto_load = False

    valid, message = validate_symbol(symbol)
    if not valid:
        st.error(message)
        st.stop()

    with st.spinner("Fetching stock data..."):
        payload = fetch_stock_data(symbol=symbol, period=period, interval=interval)

    if payload.error:
        st.error(payload.error)
        st.stop()

    cleaned = clean_history(payload.history)
    enriched = add_indicators(cleaned)
    summary = summarize_history(enriched)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Company", payload.name)
    col2.metric("Current Price", format_currency(payload.current_price, payload.currency))
    col3.metric("Rows Loaded", summary["rows"])
    col4.metric("Average Volume", format_number(summary["average_volume"]))

    st.subheader("Stock Overview")
    overview_col1, overview_col2 = st.columns(2)
    with overview_col1:
        st.write(f"**Symbol:** {payload.symbol}")
        st.write(f"**Highest High:** {format_currency(summary['highest_high'], payload.currency)}")
        st.write(f"**Lowest Low:** {format_currency(summary['lowest_low'], payload.currency)}")
    with overview_col2:
        st.write(f"**Market Cap:** {format_number(payload.market_cap)}")
        st.write(f"**Latest Close:** {format_currency(summary['latest_close'], payload.currency)}")
        st.write(f"**Volume:** {format_number(payload.volume)}")

    st.subheader("Price Trend")
    fig = create_price_figure(enriched, payload.symbol)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Historical Data")
    display_columns = [
        c for c in ["Date", "Open", "High", "Low", "Close", "Volume", "Daily Change", "Daily Return %", "MA_5", "MA_10"]
        if c in enriched.columns
    ]
    st.dataframe(enriched[display_columns], use_container_width=True, hide_index=True)

    st.subheader("Testing Notes")
    st.success(
        "This symbol loaded successfully. Try another valid symbol, a manual override, or a blank/invalid symbol to test error handling."
    )


from __future__ import annotations

import streamlit as st

from src.api import fetch_stock_data
from src.charts import create_price_figure
from src.data_processing import add_indicators, clean_history, summarize_history
from src.utils import (
    display_to_symbol,
    format_currency,
    format_number,
    get_popular_stocks,
    search_stock_catalog,
    validate_symbol,
)


st.set_page_config(
    page_title="Stock Market Analysis System",
    page_icon="📈",
    layout="wide",
)

st.title("Stock Market Analysis System")
st.caption("Use the sidebar to search popular stocks or enter a custom stock code.")

popular_df = get_popular_stocks()

with st.sidebar:
    st.header("Search")
    search_term = st.text_input(
        "Search stocks or companies",
        value="",
        placeholder="Apple, Tesla, AAPL, NVDA...",
        help="Type part of a company name or stock code.",
    )

    if search_term.strip():
        matches = search_stock_catalog(search_term, limit=20)
        if matches.empty:
            stock_code = search_term.strip().upper()
            st.caption("No catalog match. Using the text you entered as a custom stock code.")
            st.code(stock_code, language="text")
        else:
            chosen_display = st.selectbox(
                f"Matching stocks ({len(matches)})",
                matches["display"].tolist(),
                index=0,
            )
            stock_code = display_to_symbol(chosen_display)
    else:
        chosen_display = st.selectbox(
            "Popular stocks",
            popular_df["display"].tolist(),
            index=0,
        )
        stock_code = display_to_symbol(chosen_display)

    period = st.selectbox(
        "Time period",
        ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=1,
    )
    st.caption("Daily interval is used for consistency across periods.")

valid, message = validate_symbol(stock_code)
if not valid:
    st.error(message)
    st.stop()

with st.spinner(f"Fetching data for {stock_code}..."):
    payload = fetch_stock_data(symbol=stock_code, period=period, interval="1d")

if payload.error:
    st.error(payload.error)
    st.stop()

cleaned = clean_history(payload.history)
enriched = add_indicators(cleaned)
summary = summarize_history(enriched)

left, middle, right = st.columns(3)
left.metric("Selected", payload.symbol)
middle.metric("Company", payload.name)
right.metric("Current Price", format_currency(payload.current_price, payload.currency))

st.subheader("Overview")
summary_col1, summary_col2 = st.columns(2)
with summary_col1:
    st.write(f"**Latest Close:** {format_currency(summary['latest_close'], payload.currency)}")
    st.write(f"**Highest High:** {format_currency(summary['highest_high'], payload.currency)}")
    st.write(f"**Lowest Low:** {format_currency(summary['lowest_low'], payload.currency)}")
with summary_col2:
    st.write(f"**Rows Loaded:** {summary['rows']}")
    st.write(f"**Average Volume:** {format_number(summary['average_volume'])}")
    st.write(f"**Market Cap:** {format_number(payload.market_cap)}")

st.subheader("Price Trend")
fig = create_price_figure(enriched, payload.symbol)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Historical data", expanded=True):
    display_columns = [
        c for c in ["Date", "Open", "High", "Low", "Close", "Volume", "Daily Change", "Daily Return %", "MA_5", "MA_10"]
        if c in enriched.columns
    ]
    st.dataframe(enriched[display_columns], use_container_width=True, hide_index=True)

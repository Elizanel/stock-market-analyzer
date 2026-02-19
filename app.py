import streamlit as st
import yfinance as yf
import pandas as pd

# App title at the top of the page
st.title("📊 Stock Market Analyzer")

# Text input for ticker symbol (default is AAPL so the app isn't blank)
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")

# Dropdown to choose how much history to pull
period = st.selectbox("Select Timeframe:", ["1mo", "3mo", "6mo", "1y", "5y"], index=2)

# Only run the logic if the user provided a ticker
if ticker:
    try:
        # Download historical price data from Yahoo Finance
        data = yf.download(ticker, period=period, group_by="column")

        # Sometimes yfinance returns MultiIndex columns; flatten them if that happens
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        # Rename columns to be more readable in the UI
        data.rename(
            columns={
                "Open": "Opening Price",
                "High": "High Price",
                "Low": "Low Price",
                "Close": "Closing Price",
                "Volume": "Trade Volume",
            },
            inplace=True,
        )

        # Show the current columns (useful for debugging when formats change)
        st.markdown("### 📋 Current Stock Data Columns")
        for col in data.columns:
            st.write(f"- {col}")

        # Make sure we actually have a Closing Price column before doing calculations
        if "Closing Price" in data.columns:
            # Calculate a 50-day moving average of the closing price
            data["MA50"] = data["Closing Price"].rolling(window=50).mean()

            # Plot closing price + moving average
            st.subheader("📈 Price Chart with 50-Day Moving Average")
            st.line_chart(data[["Closing Price", "MA50"]])

            # Display summary stats like mean, min, max, etc.
            st.subheader("📊 Summary Statistics")
            st.write(data.describe())

            # Calculate total change over the selected period (use iloc for safe indexing)
            change = data["Closing Price"].iloc[-1] - data["Closing Price"].iloc[0]
            direction = "increased" if change > 0 else "decreased"

            # Display a simple insight sentence
            st.write(
                f"💬 {ticker} has {direction} by ${abs(change):.2f} over the selected period."
            )

        else:
            # If the expected column isn't found, stop gracefully
            st.error("❌ Could not find 'Closing Price' in the data. Try a different stock or timeframe.")

    except Exception as e:
        # Catch errors like invalid tickers, network issues, or Yahoo rate limits
        st.error(f"⚠️ Something went wrong: {e}")

    



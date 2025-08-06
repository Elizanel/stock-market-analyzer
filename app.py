import streamlit as st
import yfinance as yf
import pandas as pd

# Title
st.title("📊 Stock Market Analyzer")

# User input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")

# Timeframe selector
period = st.selectbox("Select Timeframe:", ["1mo", "3mo", "6mo", "1y", "5y"], index=2)

# Only fetch and display if a ticker is entered
if ticker:
    try:
        # Download stock data
        data = yf.download(ticker, period=period, group_by='column')

        # Flatten MultiIndex columns if they exist
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        # Rename columns for better readability
        data.rename(columns={
            "Open": "Opening Price",
            "High": "High Price",
            "Low": "Low Price",
            "Close": "Closing Price",
            "Volume": "Trade Volume"
        }, inplace=True)

        # OPTIONAL: Display column names for debugging
        st.markdown("### 📋 Current Stock Data Columns")
        # Display each column name as a bullet point or simple list
        for col in data.columns:
            st.write(f"- {col}")


        # Check that 'Closing Price' column exists
        if "Closing Price" in data.columns:
            # Calculate 50-day moving average
            data["MA50"] = data["Closing Price"].rolling(window=50).mean()

            # Display chart
            st.subheader("📈 Price Chart with 50-Day Moving Average")
            st.line_chart(data[["Closing Price", "MA50"]])

            # Show summary statistics
            st.subheader("📊 Summary Statistics")
            st.write(data.describe())

            # Summary sentence
            change = data["Closing Price"][-1] - data["Closing Price"][0]
            direction = "increased" if change > 0 else "decreased"
            st.write(f"💬 {ticker} has {direction} by ${abs(change):.2f} over the selected period.")

        else:
            st.error("❌ Could not find 'Closing Price' in the data. Try a different stock or timeframe.")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

    



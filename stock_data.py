# Import required libraries
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 


def get_stock_data(ticker): 
    """
    Download 6 months of stock price data for a given ticker symbol.
    """

    # yf.download returns a pandas DataFrame
    # with columns like: Open, High, Low, Close, Adj Close, Volume
    data = yf.download(ticker, period="6mo")

    return data 


def plot_stock_data(data, ticker):
    """
    Plot the closing price of a stock using matplotlib.
    """

    # Make sure the Close column exists before plotting
    if 'Close' not in data.columns:
        print("Close column not found.")
        return

    # Plot closing prices
    data['Close'].plot(
        title=f"{ticker} Closing Prices",
        figsize=(10, 4)
    )

    # Label axes
    plt.xlabel("Date")
    plt.ylabel("Price ($)")

    # Add grid for readability
    plt.grid()

    # Display the plot
    plt.show()



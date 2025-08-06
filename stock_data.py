#importing the libraries for info and visuals
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 

def get_stock_data(ticker): 
    data = yf.download(ticker, period="6mo")
    return data 
#Defines another function that plots the stock data using matplotlib.
def plot_stock_data(data, ticker):
    data['Close'].plot(title = f" {ticker} Closing Prices", figsize=(10,4))
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.grid()
    plt.show()




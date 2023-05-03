import yfinance as yf
import logging
from utils import config
      
def get_crypto_data():
    # Retrieve historical data from Yahoo Finance
    
    selected_ticker = config.selected_ticker
    
    print()
    print("Retrieving historical data for " + selected_ticker + "...")
    logging.debug('Retrieving historical data for %s', selected_ticker)
    ticker_data = yf.Ticker(selected_ticker)
    logging.debug('Retrieved data for %s', selected_ticker)

    # Get historical market data
    historical_data = ticker_data.history(period="max")
    logging.debug('Retrieved historical data for %s', selected_ticker)
    
    # Filter for necessary columns
    crypto_data_filtered = historical_data[["Open", "High", "Low", "Close", "Volume"]]
    logging.debug('Filtered data for %s', selected_ticker)
    
    return crypto_data_filtered
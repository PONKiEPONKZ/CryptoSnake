"""
This module contains the stop_loss_order function for implementing the stop loss strategy. It takes in the current price of an asset and a percentage for the stop loss. It calculates and returns the stop loss price based on the percentag
"""

# stop_loss.py

def stop_loss_order(crypto_data, stop_loss_percent, last_close_price):
    last_close_price = crypto_data.iloc[-1]['Close']
    stop_loss_price = last_close_price * (1 - stop_loss_percent / 100)

    return stop_loss_price


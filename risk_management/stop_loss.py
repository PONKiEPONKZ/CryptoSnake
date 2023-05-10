"""
This module contains the stop_loss_order function for implementing the stop loss strategy. It takes in the current price of an asset and a percentage for the stop loss. It calculates and returns the stop loss price based on the percentag
"""

# stop_loss.py

def stop_loss_order(Close, stop_loss_percent):
    stop_loss_price = float(Close) * (1 - stop_loss_percent / 100)

    return stop_loss_price


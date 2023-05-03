"""
This module contains the stop_limit_order function for implementing the stop limit strategy. It takes in the current price of an asset, a percentage for the stop loss, and a percentage for the limit price. It calculates and returns both the stop loss price and the limit price based on the percentages.
"""

# stop_limit.py

def stop_limit_order(price, stop_loss_percent, limit_percent):
    stop_loss_price = price * (1 - stop_loss_percent / 100)
    limit_price = price * (1 + limit_percent / 100)
    return stop_loss_price, limit_price


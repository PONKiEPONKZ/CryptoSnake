"""
This module contains the calculate_portfolio_allocation function for calculating the allocation amounts for a portfolio. It takes in an investment amount and a list of allocation percentages for each asset in the portfolio. It checks if the total allocation percentage is not more than 100 and calculates the allocation amount for each asset based on the percentage. It returns a list of allocation amounts for each asset.
"""

# diversification.py

def calculate_portfolio_allocation(investment_amount, allocation_percentages):
    total_allocation = sum(allocation_percentages)
    if total_allocation > 100:
        raise ValueError('Total allocation cannot exceed 100%')
    allocation_amounts = [investment_amount * p / 100 for p in allocation_percentages]
    return allocation_amounts


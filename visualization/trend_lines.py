import matplotlib.pyplot as plt
import numpy as np

class TrendLines:
    def __init__(self):
        pass

    def plot_trend_line(self, crypto_data):
        # extract closing prices from the crypto data        
        close_prices = crypto_data["Close"]

        # create x and y arrays for linear regression
        x = np.array(range(len(close_prices)))
        y = np.array(close_prices)

        # fit a linear regression line to the data
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        trendline = polynomial(x)

        # plot the data and trend line
        fig, ax = plt.subplots()
        ax.plot(x, y, label='Data')
        ax.plot(x, trendline, '--', label='Trend line')
        ax.legend()
        plt.show()
        
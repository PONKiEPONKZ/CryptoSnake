from visualization.trend_lines import TrendLines
from visualization.candlestick_charts import CandlestickCharts
from utils.config import selected_ticker as config_selected_ticker
from utils.config import show_loading_animation
from utils.logger import Logger
from utils.ticker_selector import retrieve_ticker
from utils.config import api_key, api_secret, base_url, log_file
from utils import config
from risk_management.diversification import calculate_portfolio_allocation
from risk_management.stop_limit import stop_limit_order
from risk_management.stop_loss import stop_loss_order
from machine_learning.models.lstm_model.lstm import LSTMModel
from machine_learning.prep.ml_prep import prepare_data
from machine_learning.prep.ml_scaler import MLScaler
from machine_learning.models.random_forest.random_forest import RandomForestModel
from machine_learning.models.gru.gru import GRUModel
from machine_learning.models.regression.regression import RegressionModel
from machine_learning.models.decision_tree.decision_tree import DecisionTree
from machine_learning.models.neural_network.neural_network import NeuralNetwork
from data_analysis.sentiment_analysis import SentimentalAnalysis
from data_analysis.fundamental_analysis import FundamentalAnalysis
from data_analysis.technical_analysis import perform_technical_analysis
from data_collection.social_media_data import get_twitter_data
from data_collection.news_data import get_news_data
from data_collection.crypto_data import get_crypto_data
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pandas as pd
import sys
import numpy as np
import plotly.graph_objs as go

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


# Set the display format
pd.options.display.float_format = "{:.10f}".format

logger = Logger()

tf.get_logger().setLevel("ERROR")


def main():
    try:
        # Log start of program
        print()
        print()
        print("** Welcome to CryptoSnake **")
        print()
        print()
        logger.log_info("Program started")

        # Use the selector to select a ticker and store it's logo
        ticker = retrieve_ticker(config)

        # Get historical data using the yFinance API
        logger.log_info("Collecting crypto data from online resources...")
        crypto_data = get_crypto_data()
        print("Done.")
        print()
        null_locations = crypto_data.isnull()
        print(null_locations)

        # Perform data analysis on the collected historical data
        logger.log_info("Performing data analysis")
        technical_analysis_results = perform_technical_analysis(crypto_data)
        print("Done.")
        print()

        # Get news articles using the newsdata.io API
        logger.log_info("Collecting news articles from online resources...")
        news_data = get_news_data()
        print("Done.")
        print()

        # Perform sentiment analysis
        logger.log_info("Performing sentiment analysis")
        sa = SentimentalAnalysis()
        sentiment_score = sa.get_news_sentiment(news_data)
        print(f"News sentiment score for {config.selected_ticker} is {sentiment_score}")
        logger.log_info(f"News sentiment score for {config.selected_ticker} is {sentiment_score}")
        # social_media_data = get_twitter_data()

        fundamental_analysis_results = FundamentalAnalysis()

        # Visualize collected data
        #logger.log_info("Visualizing data")
        #print("Generating chart...")

        # Creating candlestick chart
        crypto_data_df = pd.DataFrame(data=crypto_data, columns=[
                                      "Open", "High", "Low", "Close", "Volume"])
        candlestick_charts = CandlestickCharts()
        fig = candlestick_charts.plot_candlestick_chart(
            crypto_data_df, technical_analysis_results
        )
        
        #trend_lines = TrendLines()
        #if  'xaxis' in fig.update_layout():
        #    ax=fig.update_layout['xaxis']['domain']
        #else:
        #    logger.log_warning("xaxis not found in figure layout")
        #fig = trend_lines.plot_trend_lines(crypto_data, candlestick_charts)
        # Prepare data for machine learning and split the crypto data into features (X) and target (y)
        logger.log_info("Splitting the crypto data into features (X) and target (y)")
        X_train, X_test, y_train, y_test = prepare_data(crypto_data)

        # create an instance of the MLScaler class
        scaler = MLScaler()

        # Scale the data using the training data
        logger.log_info("Scaling the data using the training data")
        X_train_scaled, X_test_scaled = scaler.scale_data(X_train, X_test)

        # Convert DataFrames to numpy arrays
        X_train_scaled_np = np.array(X_train_scaled)
        X_test_scaled_np = np.array(X_test_scaled)
        print("X_train_scaled_np shape:", X_train_scaled_np.shape)
        print("X_test_scaled_np shape:", X_test_scaled_np.shape)

        # Create an instance of LSTM model
        model = LSTMModel()

        # Train the model using the scaled training data
        print()
        print("Training the LSTM model...")
        model.train(X_train_scaled_np)

        # Make predictions using the scaled test data
        print()
        print("Making predictions on the scaled data")
        print()
        predictions_scaled = model.predict(X_test_scaled_np)
        print("predictions_scaled shape:", predictions_scaled.shape) # <-- add this line to print the shape of predictions_scaled

        # Unscale the predicted values
        print()
        print("Unscaling the data")
        predictions_unscaled = scaler.unscale_data(predictions_scaled.reshape(-1, 1))

        #predictions_unscaled = scaler.unscale_data(predictions_scaled)

        # Convert DataFrames to numpy arrays
        #X_test_np = np.array(X_test_scaled_np)
        #y_test_np = np.array(y_test_scaled_np)

        # Evaluate the model on the unscaled test set
        print()
        print("Evaluating model...")
        #mse = model.evaluate(X_test_scaled_np)
        # Evaluate the model on the test data
        mse = model.evaluate(X_test_scaled_np, scaler.unscale_data(y_test))


        logger.log_info(f"Mean squared error on test set: {mse}")
        print(f"Mean squared error on test set: {mse}")

        # create a range of dates for the predicted values
        start_date = crypto_data.index[0]
        end_date = crypto_data.index[-1]
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        # create a trace for the predicted values
        predicted_trace = go.Scatter(x=date_range, y=predictions_unscaled.flatten(), name='Predicted')

        # add the predicted trace to the figure data
        print("Generating charts...")
        fig = go.Figure()
        fig.add_trace(predicted_trace)
        fig.update_layout(title="LSTM Prediction")
        fig.show()

        # Extractng last closing prices
        last_close_price = crypto_data.iloc[-1]['Close']

        # Apply risk management strategies
        print("Applying risk management strategies...")
        logger.log_info("Applying risk management strategies")
        stop_loss_order(crypto_data, config.stop_loss_threshold, last_close_price)
        stop_limit_order(config.stop_limit_threshold, last_close_price, limit_percent=2)
        calculate_portfolio_allocation(crypto_data, config.portfolio_size)

        # Log results
        logger.log_info("Successfully executed all tasks.")
    except Exception as e:
        # Log the error
        logger.log_exception(f"An error occurred: {str(e)}")

        # Exit with a non-zero exit code to indicate that an error occur        sys.exit(1)


if __name__ == "__main__":
    main()
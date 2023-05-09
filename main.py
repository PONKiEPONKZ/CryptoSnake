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
from machine_learning.lstm_model.lstm import LSTMModel
from machine_learning.random_forest.random_forest import RandomForestModel
from machine_learning.gru.gru import GRUModel
from machine_learning.regression.regression import RegressionModel
from machine_learning.decision_tree.decision_tree import DecisionTree
from machine_learning.neural_network.neural_network import NeuralNetwork
from data_analysis.sentiment_analysis import SentimentalAnalysis
from data_analysis.fundamental_analysis import FundamentalAnalysis
from data_analysis.technical_analysis import perform_technical_analysis
from data_collection.social_media_data import get_twitter_data
from data_collection.news_data import get_news_data
from data_collection.crypto_data import get_crypto_data
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
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
        logger.log_info("Visualizing data")
        print("Generating chart...")

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

        # Prepare data for machine learning
        logger.log_info("Training machine learning models")
        X = crypto_data_df.drop(["Close"], axis=1)
        y = crypto_data_df["Close"]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train the neural network model
        trained_neural_network_model = NeuralNetwork(
            input_size=X_train.shape[1], output_size=1
        )
        trained_neural_network_model.train(X_train, y_train)

        # Predict on the trained neural network test data
        y_pred = trained_neural_network_model.predict(X_test)

        # Create a new trace for the predicted values
        trace_pred = go.Scatter(
            x=X_test.index, y=y_pred.flatten(), name='Predicted')

        # Add the new trace to the existing fig object
        fig.add_trace(trace_pred)

        # Update the figure layout and show the chart
        fig.update_layout(title='My Chart with Predicted Values')
        fig.show()

        # Extract the features and labels from the crypto_data
        crypto_data["Date"] = crypto_data.index.astype('int64') // 10**9
        features = crypto_data[["Date", "Open",
                                "High", "Low", "Volume"]].values
        close_diff = np.diff(crypto_data["Close"].values)
        labels = np.concatenate([[0], np.sign(close_diff)])

        # Create a dictionary with the features and labels
        data = {"features": features, "labels": labels}

        # Define your pipeline with the SimpleImputer transformer
        pipeline = Pipeline(
            [
                (
                    "imputer",
                    SimpleImputer(strategy="mean"),
                ),  # Replace missing values with the mean of each feature
                (
                    "scaler",
                    StandardScaler(),
                ),  # Scale the features to zero mean and unit variance
                # Train a logistic regression model
                ("clf", LogisticRegression()),
            ]
        )

        # Fit the pipeline to your training data
        pipeline.fit(X_train, y_train)

        # Use the fitted pipeline to predict on new data
        y_pred = pipeline.predict(X_test)

        # Train the decision tree on the data
        decision_tree = DecisionTree()
        decision_tree.train(data)

        # Test the model
        test_data = get_test_data()
        test_features = test_data[[
            "Open", "High", "Low", "Volume", "Date"]].values
        test_labels = np.sign(np.diff(test_data["Close"].values))
        test_data = {"features": test_features, "labels": test_labels}
        accuracy = test_model(decision_tree, test_data)

        print(f"Accuracy: {accuracy:.2f}")
        if accuracy < 0.5:
            print(
                "Model is not performing well. You may want to try a different model or adjust the hyperparameters."
            )
            sys.exit(1)

        trained_regression_model = RegressionModel.train(crypto_data)

        # Apply risk management strategies
        logger.log_info("Applying risk management strategies")
        stop_loss_order(crypto_data, config.stop_loss_threshold)
        stop_limit_order(crypto_data, config.stop_limit_threshold)
        calculate_portfolio_allocation(crypto_data, config.portfolio_size)

        # Log results
        logger.log_info("Successfully executed all tasks.")
    except Exception as e:
        # Log the error
        logger.log_exception(f"An error occurred: {str(e)}")

        # Exit with a non-zero exit code to indicate that an error occurred
        sys.exit(1)


if __name__ == "__main__":
    main()

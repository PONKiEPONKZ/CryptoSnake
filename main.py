import logging
import sys
import numpy as np
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')


from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from data_collection.crypto_data import get_crypto_data
from data_collection.news_data import get_news_data
from data_collection.social_media_data import get_twitter_data
from data_analysis.technical_analysis import perform_technical_analysis
from data_analysis.fundamental_analysis import FundamentalAnalysis
from data_analysis.sentiment_analysis import SentimentalAnalysis
from machine_learning.neural_network import NeuralNetwork
from machine_learning.decision_tree import DecisionTree
from machine_learning.regression_model import RegressionModel
from machine_learning.gru_model import GRUModel
from machine_learning.random_forest_model import RandomForestModel
from machine_learning.lstm_model import LSTMModel
from risk_management.stop_loss import stop_loss_order
from risk_management.stop_limit import stop_limit_order
from risk_management.diversification import calculate_portfolio_allocation

from utils import config
from utils.config import api_key, api_secret, base_url, log_file, selected_ticker
from utils.ticker_selector import retrieve_ticker
from utils.config import selected_ticker as config_selected_ticker
from visualization.candlestick_charts import CandlestickCharts
from visualization.trend_lines import TrendLines


def main():
    try:
        # Log start of program
        print()
        print()
        print("** Welcome to CryptoSnake **")
        print()
        print()
        logging.info("Program started.")    
       
        # Use the ticker selector to select a ticker
        ticker = retrieve_ticker(config)
                
        # Set the display format
        pd.options.display.float_format = '{:.10f}'.format

        # Get historical data using the yFinance API
        logging.info("Collecting crypto data from online resources...")
        crypto_data = get_crypto_data()
        print("Done.")
        print()
        null_locations = crypto_data.isnull()
        
        #Get news articles using the newsdata.io API
        logging.info('Collecting news articles from online resources...')
        news_data = get_news_data()
        print("Done.")
        print()

        # social_media_data = get_twitter_data()

        # Perform data analysis on the collected historical data
        logging.info('Performing data analysis')        
        technical_analysis_results = perform_technical_analysis(crypto_data)
        print("Done.")
        print()
       
        #Perform sentiment analysis
        logging.info('Performing sentiment analysis')
        sa = SentimentalAnalysis()
        sentiment_score = sa.get_news_sentiment()
        print("Sentiment score:", sentiment_score)

        fundamental_analysis_results = FundamentalAnalysis()

        # Visualize collected data
        logging.info("Visualizing data")
        print("Generating chart...")

        candlestick_charts = CandlestickCharts()
        candlestick_charts.plot_candlestick_chart(crypto_data, technical_analysis_results)
        trend_lines = TrendLines()
        trend_lines.plot_trend_line(crypto_data)
        
        # Train machine learning models
        logging.info('Training machine learning models')
        X = crypto_data.drop(['Close'], axis=1).values
        y = crypto_data['Close'].values
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        trained_neural_network = NeuralNetwork(input_size=X_train.shape[1], output_size=1)
        trained_neural_network.train(X_train, y_train)

        # Extract the features and labels from the crypto_data
        crypto_data['Date'] = crypto_data.index.astype(int) // 10**9
        features = crypto_data[['Date', 'Open', 'High', 'Low', 'Volume']].values
        close_diff = np.diff(crypto_data['Close'].values)
        labels = np.concatenate([[0], np.sign(close_diff)])

        # Create a dictionary with the features and labels
        data = {'features': features, 'labels': labels}
        
        # Define your pipeline with the SimpleImputer transformer
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),  # Replace missing values with the mean of each feature
            ('scaler', StandardScaler()),                 # Scale the features to zero mean and unit variance
            ('clf', LogisticRegression())                 # Train a logistic regression model
        ])

        # Fit the pipeline to your training data
        pipeline.fit(X_train, y_train)

        # Use the fitted pipeline to predict on new data
        y_pred = pipeline.predict(X_test)

        # Train the decision tree on the data
        decision_tree = DecisionTree()
        decision_tree.train(data)

        # Test the model
        test_data = get_test_data()
        test_features = test_data[['Open', 'High', 'Low', 'Volume', 'Date']].values
        test_labels = np.sign(np.diff(test_data['Close'].values))
        test_data = {'features': test_features, 'labels': test_labels}
        accuracy = test_model(decision_tree, test_data)

        print(f"Accuracy: {accuracy:.2f}")
        if accuracy < 0.5:
            print(
                "Model is not performing well. You may want to try a different model or adjust the hyperparameters."
            )
            sys.exit(1)

        trained_regression_model = RegressionModel.train(crypto_data)

        # Apply risk management strategies
        logging.info("Applying risk management strategies")
        stop_loss_order(crypto_data, config.stop_loss_threshold)
        stop_limit_order(crypto_data, config.stop_limit_threshold)
        calculate_portfolio_allocation(crypto_data, config.portfolio_size)

        # Log results
        logging.info("Successfully executed all tasks.")
    except Exception as e:
        # Log the error
        logging.exception("An error occurred: %s", str(e))

        # Exit with a non-zero exit code to indicate that an error occurred
        sys.exit(1)

if __name__ == '__main__':
    main()

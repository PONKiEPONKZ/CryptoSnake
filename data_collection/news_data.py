"""
This module contains the get_news_data function for fetching news articles related to a given query from the News API. It constructs the API URL using the selected_ticker and the API key, and sends a GET request to the API. If the response status code is 200, it parses the response JSON and returns the list of articles. If the status code is not 200, it prints an error message and returns None.
"""

import requests
from utils import config

def get_news_data():
    api_key = config.api_key
    selected_ticker = config.selected_ticker

    print("Retrieving news articles for " + selected_ticker + "...")

    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={selected_ticker}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success' and data['totalResults'] > 0:
            return data['results']
            print("News sentiment data:")
            print(news_sentiment_data.head(), "\n")
        else:
            print("No news data found.\n")
    else:
        print("Error fetching news data.\n")

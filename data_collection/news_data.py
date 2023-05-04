"""
This module contains the get_news_data function for fetching news articles related to a given query from the News API. It constructs the API URL using the selected_ticker and the API key, and sends a GET request to the API. If the response status code is 200, it parses the response JSON and returns the list of articles. If the status code is not 200, it prints an error message and returns None.
"""

import requests
from utils import config
from utils.config import selected_ticker

def get_news_data():
    api_key = config.api_key
    
    print("Retrieving news articles for " + config.selected_ticker + "...")

    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={config.selected_ticker}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success' and data['totalResults'] > 0:
            return data['results']
              
        else:
            print("No news data found.\n")
    else:
        print("Error fetching news data.\n")

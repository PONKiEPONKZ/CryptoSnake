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

def get_news_sentiment():
    news_data = get_news_data()
    
    if news_data:
        print("News sentiment data:")
        for article in news_data:
            # do sentiment analysis on article['title'] and article['description']
            # and print the sentiment score
            print(article['title'])
            print(article['description'])
            print("Sentiment score: x\n")
    else:
        print("No news data found.\n")

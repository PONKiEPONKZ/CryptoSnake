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
            # Filter out articles without a title or description
            results = [article for article in data['results'] if article.get('title') and article.get('description')]
            return results
              
        else:
            print("No news data found.\n")
    else:
        print("Error fetching news data.\n")
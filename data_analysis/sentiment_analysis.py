from textblob import TextBlob
from data_collection.news_data import get_news_data
from utils import config
from utils.logger import Logger

class SentimentalAnalysis:
    def __init__(self):
        self.logger = Logger()
    
    # function to calculate the sentiment score of a given text
    def get_sentiment_score(self, text):
        try:
            blob = TextBlob(text) 
            return blob.sentiment.polarity
        except Exception as e:
            self.logger.log_error(f"Error getting sentiment score: {str(e)}")
            return 0

    # function to get the sentiment score of news related to a given symbol
    def get_news_sentiment(self, news_data):
        sentiment_score = 0
        selected_ticker = config.selected_ticker
        try:
            for article in news_data:
                if article is not None and "title" in article:
                    if selected_ticker.upper() in article["title"] or selected_ticker.upper().replace("-USD", "") in article["title"]:
                        sentiment_score += self.get_sentiment_score(article["title"])
                    try:
                        if selected_ticker.upper() in article["description"] or selected_ticker.upper().replace("-USD", "") in article["description"]:
                            sentiment_score += self.get_sentiment_score(article["description"])
                    except KeyError:
                        pass
        except Exception as e:
            self.logger.log_error(f"Error getting news sentiment score: {str(e)}")
            return 0
        return sentiment_score

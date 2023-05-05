import logging
from textblob import TextBlob
from data_collection.news_data import get_news_data
from utils import config

class SentimentalAnalysis:
    def __init__(self):
        pass

    def get_sentiment_score(self, text):
        # function to calculate the sentiment score of a given text
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def get_news_sentiment(self, news_data):
        # function to get the sentiment score of news related to a given symbol
        sentiment_score = 0
        selected_ticker = config.selected_ticker
        if not selected_ticker.endswith("-USD"):
            selected_ticker += "-USD"
        for article in news_data:
            if (
                article is not None
                and ("title" in article and selected_ticker.upper() in article["title"])
                or (
                    "description" in article
                    and selected_ticker.upper() in article["description"]
                )
            ):
                sentiment_score += self.get_sentiment_score(article["title"])
                sentiment_score += self.get_sentiment_score(article["description"])
        return sentiment_score

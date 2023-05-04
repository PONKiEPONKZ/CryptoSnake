from textblob import TextBlob
import logging

class SentimentalAnalysis:
    def __init__(self):
        pass

    def get_sentiment_score(self, text):
        # function to calculate the sentiment score of a given text
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def get_news_sentiment(self, symbol, news_data):
        # function to get the sentiment score of news related to a given symbol
        sentiment_score = 0
        for article in news_data:
            if article is not None and ('title' in article and symbol.upper() in article['title']) or ('description' in article and symbol.upper() in article['description']):
                sentiment_score += self.get_sentiment_score(article['title'])
                sentiment_score += self.get_sentiment_score(article['description'])
        return sentiment_score

    print("Performing sentiment anaylsis...")
    
def main():
    try:
        #Perform sentiment analysis
        logging.info('Performing sentiment analysis')
        sa = SentimentalAnalysis()
        symbol = 'BTC' # just for testing purposes
        news_data = [{'title': 'BTC soars to new heights', 'description': 'The price of BTC has reached a new all-time high.'}] # just for testing purposes
        sentiment_score = sa.get_news_sentiment(symbol, news_data)
        print("Sentiment score:", sentiment_score) 
    except Exception as e:
        logging.exception(f"Error in sentiment analysis: {e}")
        sys.exit(1)
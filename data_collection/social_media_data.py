from utils import config
from utils.config import selected_ticker
from bs4 import BeautifulSoup
import requests


# Scraping Twitter data
def get_twitter_data():
    query = selected_ticker
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.find_all('div', {'data-testid': 'tweet'})
    data = []
    for tweet in tweets:
        tweet_text = tweet.find('div', {'class': 'css-901oao css-bfa6kz r-111h2gw r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-13tjlyg r-1pi2tsx r-1xcajam r-1pjcn9w r-11wrixw r-61z16t r-1tl8opc r-1s3sdrz r-13qz1uu'}).get_text()
        user = tweet.find('a', {'class': 'css-4rbku5 css-18t94o4 css-901oao r-111h2gw r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0'}).get_text()
        retweets = tweet.find('div', {'data-testid': 'retweet'}).get_text()
        likes = tweet.find('div', {'data-testid': 'like'}).get_text()
        created_at = tweet.find('time', {'datetime': True})['datetime']
        data.append({
            'text': tweet_text,
            'user': user,
            'retweets': retweets,
            'likes': likes,
            'created_at': created_at
        })

    return data

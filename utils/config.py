import os
import sys
import time


# Path to the root directory (CryptoSnakeV2)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define loading animation


def show_loading_animation():
    animation = "|/-\\"
    idx = 0
    while True:
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        sys.stdout.flush()
        time.sleep(0.1)


# Path to the log file in the root directory
log_file = os.path.join(ROOT_DIR, 'app.log')

# selected_ticker configuration


def set_selected_ticker(value):
    global selected_ticker
    selected_ticker = value


selected_ticker = None


# selected_ticker_image_url configuration
def set_selected_ticker_image_url(value):
    global selected_ticker_image_url
    selected_ticker_image_url = value


selected_ticker_image_url = None


# API keys and other configurations
api_key = 'pub_2112721cdad7223a39b4dea7d16f609f1b639'
api_secret = ''
base_url = ''
TWITTER_API_KEY = 'Fdq7nQsLLBAbxZfVJakKYCf7f'
TWITTER_API_SECRET = 'jNWCXn9cPlfZY5nmotJBTRe8PwLNlmQwHTybaFTc97tGsVBNCS'
TWITTER_ACCESS_TOKEN = '1471859951664603138-sK5YaEQUP04s3gPmSueLVCyjbg9oya'
TWITTER_ACCESS_SECRET = '76HUS3YBCxFZRW6j9Qk4CFao6wa4KI59Gdgi1Ssgu4DvB'

PLOT_HEIGHT = 800

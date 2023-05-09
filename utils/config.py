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

# Setting for the graphs
TICK_FONT_COLOR = "#FFFFFF" # white
SPIKE_COLOR = "#6495ED" # cornflower blue
AXIS_BG_COLOR = "#2E2E2E" # dark gray
LINE_COLOR = "#FFFFFF" # white
TITLE_FONT_COLOR = "#FFFFFF" # white
PLOT_BG_COLOR = "#2a2e39" # midnight blue
PAPER_BG_COLOR = "#000000" # white
GRID_COLOR = "#A9A9A9" # dark gray
ZEROLINE_COLOR = "#FFFF00" # yellow
AXIS_FONT_COLOR = "#FFFFFF" # white
AXIS_TITLE_COLOR = "#FFFFFF" # white
OVERBOUGHT_COLOR = "#FF0000" # red
OVERSOLD_COLOR = "#008000" # green
BULLISH_COLOR = "#008000" # green
BEARISH_COLOR = "#FF0000" # red
VOLUME_COLOR_MAPPING = {
"increase": "#008000", # green
"decrease": "#FF0000", # red
"static": "#FFA500" # orange
}

PLOT_HEIGHT = 800

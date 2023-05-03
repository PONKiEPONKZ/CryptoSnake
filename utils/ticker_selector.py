import requests
from utils import config
from .config import selected_ticker

print()
print("Select a coin from the list:")

def retrieve_ticker(config):
    # Retrieve the top 50 cryptocurrencies by market cap
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": "50",
        "page": "1",
        "sparkline": "false"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValueError("Error retrieving tickers.")

    data = response.json()
    ticker_list = [coin["symbol"].upper() for coin in data]

    # Split the ticker list into 5 columns with 10 elements each
    num_cols = 5
    col_width = 10
    num_rows = len(ticker_list) // num_cols 

    # Loop through each row and print the corresponding elements from each column
    for row in range(num_rows):
        for col in range(num_cols):
            index = row + col * num_rows
            if index < len(ticker_list):
                print(f"{index+1:<2}. {ticker_list[index]:<{col_width}}", end=" "*col_width)
            else:
                print(" "*col_width, end=" "*col_width)
        print()

    while True:
        try:
            print()
            choice = int(input("Enter a number between 1 and 50: "))
            if 1 <= choice <= 50:
                break
            else:
                print()
                print("Invalid choice. Please enter a number between 1 and 50.")
        except ValueError:
            print()
            print("Invalid choice. Please enter a number between 1 and 50.")

    # Set the chosen ticker symbol
    selected_ticker_value = ticker_list[choice-1] + "-USD"
    config.selected_ticker = selected_ticker_value

    return selected_ticker_value

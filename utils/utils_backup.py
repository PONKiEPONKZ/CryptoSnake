import requests
import pandas as pd
from config import API_KEY, API_SECRET, BASE_URL


def get_data(symbol, start_date, end_date):
    url = f'{BASE_URL}/v1/candles/{symbol}/history'
    params = {'from': start_date, 'to': end_date}
    headers = {'api-key': API_KEY, 'api-secret': API_SECRET}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df


def save_data(df, filename):
    df.to_csv(filename, index=False)


def load_data(filename):
    df = pd.read_csv(filename)
    df['time'] = pd.to_datetime(df['time'])
    return df


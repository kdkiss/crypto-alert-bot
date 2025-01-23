# File: bybit_alert_bot/api/bybit_api.py

import requests

BYBIT_API_URL = 'https://api.bybit.com/v5/market/tickers'
BYBIT_KLINE_URL = 'https://api.bybit.com/v5/market/kline'

def fetch_price(symbol):
    """
    Fetches the current price of the given symbol from Bybit API.
    :param symbol: The trading pair symbol (e.g., "BTC").
    :return: Current price as a float or None if not found.
    """
    symbol = f"{symbol.upper()}USDT"
    response = requests.get(BYBIT_API_URL, params={'category': 'linear', 'symbol': symbol})
    data = response.json()
    if 'result' in data and 'list' in data['result']:
        for ticker in data['result']['list']:
            if ticker['symbol'] == symbol:
                return float(ticker['lastPrice'])
    return None

def fetch_tickers():
    """
    Fetches the list of all tickers from the Bybit API.
    :return: List of tickers or an empty list if the API call fails.
    """
    response = requests.get(BYBIT_API_URL, params={'category': 'linear'})
    data = response.json()
    if 'result' in data and 'list' in data['result']:
        return data['result']['list']
    return []

def fetch_historical_prices(symbol, interval='15', limit=100):
    """
    Fetches historical prices (candlestick data) for a given symbol.
    :param symbol: The trading pair symbol (e.g., "BTC").
    :param interval: Candlestick interval (e.g., "15" for 15 minutes).
    :param limit: Number of data points to fetch.
    :return: List of closing prices or None if not found.
    """
    response = requests.get(
        BYBIT_KLINE_URL,
        params={
            'category': 'linear',
            'symbol': f"{symbol.upper()}USDT",
            'interval': interval,
            'limit': limit
        }
    )
    data = response.json()
    if 'result' in data and 'list' in data['result']:
        # Extract the closing prices from the kline data
        return [float(item[4]) for item in data['result']['list']]  # [4] is the closing price
    return None


# File: bybit_alert_bot/utils/rsi.py

def calculate_rsi(prices, period=14):
    """
    Calculates the Relative Strength Index (RSI).
    :param prices: List of closing prices.
    :param period: Look-back period for RSI calculation.
    :return: RSI value as a float.
    """
    if len(prices) < period:
        raise ValueError("Not enough data to calculate RSI.")

    # Calculate price changes
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    # Separate gains and losses
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]

    # Calculate average gains and losses
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Compute RSI
    for i in range(period, len(deltas)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

    if avg_loss == 0:
        return 100  # Max RSI if no losses

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

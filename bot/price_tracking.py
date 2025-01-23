# File: bybit_alert_bot/bot/price_tracking.py

import threading
import time
from api.bybit_api import fetch_tickers
from db.db_operations import get_alerts, remove_alert

def start_price_tracking(bot, conn):
    """
    Starts a background thread for tracking prices and processing alerts.
    """
    cursor = conn.cursor()

    def tracking_loop():
        while True:
            try:
                tickers = fetch_tickers()
                if tickers:
                    alerts = get_alerts(cursor)
                    for alert_id, user_id, symbol, target_price, condition in alerts:
                        full_symbol = f"{symbol.upper()}USDT"
                        for ticker in tickers:
                            if ticker['symbol'] == full_symbol:
                                current_price = float(ticker['lastPrice'])
                                if (condition == 'below' and current_price < target_price) or \
                                   (condition == 'above' and current_price > target_price):
                                    bot.send_message(
                                        user_id,
                                        f"Price alert hit! {full_symbol} {condition} {target_price}. Current: {current_price}."
                                    )
                                    remove_alert(cursor, conn, alert_id)
            except Exception as e:
                print(f"Error in price tracking: {e}")
            time.sleep(15)

    threading.Thread(target=tracking_loop, daemon=True).start()

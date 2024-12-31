import telebot
import sqlite3
import requests
import threading
import time
# Import the token from config.py
from config import API_TOKEN

BYBIT_API_URL = 'https://api.bybit.com/v5/market/tickers'
bot = telebot.TeleBot(API_TOKEN)

# Database setup
conn = sqlite3.connect('alerts.db', check_same_thread=False)
cursor = conn.cursor()

# Drop existing table if the schema is incorrect (optional: use this for debugging)
# cursor.execute('DROP TABLE IF EXISTS alerts')

# Update schema: Add 'condition' column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        price REAL NOT NULL,
        condition TEXT NOT NULL
    )
''')
conn.commit()


# Command: /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /help to see available commands.")

# Command: /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Start the bot and get a welcome message.\n"
        "/alert [symbol] [price] - Set a price alert. Example: /alert BTC 30000\n"
        "/listalerts - List all your active alerts.\n"
        "/deletealert [id] - Delete an alert by its ID.\n"
        "/p [symbol] - Get the current price of a trading pair. Example: /p BTC\n"
        "/stop - Stop the bot.\n"
        "/help - Show this help message."
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['alert'])
def set_alert(message):
    try:
        _, symbol, price, condition = message.text.split()
        price = float(price)
        if condition.lower() not in ['below', 'above']:
            bot.reply_to(message, "Condition must be 'below' or 'above'.")
            return
        
        cursor.execute(
            'INSERT INTO alerts (user_id, symbol, price, condition) VALUES (?, ?, ?, ?)', 
            (message.from_user.id, symbol.upper(), price, condition.lower())
        )
        conn.commit()
        bot.reply_to(message, f"Alert set for {symbol.upper()} at {price} ({condition.lower()}).")
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /alert [symbol] [price] [below/above].")



@bot.message_handler(commands=['listalerts'])
def list_alerts(message):
    try:
        cursor.execute('SELECT id, symbol, price FROM alerts WHERE user_id = ?', (message.from_user.id,))
        alerts = cursor.fetchall()
        if alerts:
            response = "Your alerts:\n" + "\n".join([f"{id}: {symbol} at {price}" for id, symbol, price in alerts])
        else:
            response = "No active alerts."
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error listing alerts: {str(e)}")


# Command: /deletealert
@bot.message_handler(commands=['deletealert'])
def delete_alert(message):
    try:
        _, alert_id = message.text.split()
        cursor.execute('DELETE FROM alerts WHERE id = ? AND user_id = ?', 
                       (int(alert_id), message.from_user.id))
        conn.commit()
        bot.reply_to(message, "Alert deleted.")
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /deletealert [id].")

# Command: /p
@bot.message_handler(commands=['p'])
def get_price(message):
    try:
        _, symbol = message.text.split()
        symbol = f"{symbol.upper()}USDT"  # Append USDT to the input symbol
        response = requests.get(BYBIT_API_URL, params={'category': 'linear', 'symbol': symbol})
        data = response.json()
        if 'result' in data and data['result']['list']:
            for ticker in data['result']['list']:  # Access 'list' under 'result'
                if ticker['symbol'] == symbol:
                    bot.reply_to(message, f"Current price of {symbol}: {ticker['lastPrice']}")
                    return
        bot.reply_to(message, f"Symbol {symbol} not found.")
    except Exception as e:
        bot.reply_to(message, f"Error fetching price. {str(e)}")

def price_tracking():
    while True:
        try:
            response = requests.get(BYBIT_API_URL, params={'category': 'linear'})
            data = response.json()
            if 'result' in data and data['result']['list']:
                cursor.execute('SELECT id, user_id, symbol, price, condition FROM alerts')
                alerts = cursor.fetchall()

                for alert_id, user_id, symbol, target_price, condition in alerts:
                    full_symbol = f"{symbol.upper()}USDT"
                    for ticker in data['result']['list']:
                        if ticker['symbol'] == full_symbol:
                            current_price = float(ticker['lastPrice'])
                            print(f"Processing alert {alert_id}: {full_symbol} at {current_price}, target {target_price} ({condition})")
                            
                            # Trigger alert based on condition
                            if condition == 'below' and current_price < target_price:
                                bot.send_message(user_id, f"Price alert hit! {full_symbol} dropped below {target_price}. Current: {current_price}.")
                                cursor.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
                                conn.commit()
                            elif condition == 'above' and current_price > target_price:
                                bot.send_message(user_id, f"Price alert hit! {full_symbol} rose above {target_price}. Current: {current_price}.")
                                cursor.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
                                conn.commit()
        except Exception as e:
            print(f"Error in price tracking: {e}")
        time.sleep(15)  # Check every 5 seconds



# Start the price tracking in a separate thread
threading.Thread(target=price_tracking, daemon=True).start()

# Command: /stop
@bot.message_handler(commands=['stop'])
def stop_interaction(message):
    bot.reply_to(message, "Goodbye!")

# Polling
bot.polling()

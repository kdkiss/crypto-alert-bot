# File: bybit_alert_bot/bot/commands.py

from telebot import TeleBot
from api.bybit_api import fetch_price
from db.db_operations import add_alert, list_alerts, remove_alert
from utils.rsi import calculate_rsi
from api.bybit_api import fetch_historical_prices


def register_commands(bot: TeleBot, conn):
    """
    Registers all bot commands.
    :param bot: The TeleBot instance.
    :param conn: The database connection.
    """
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Welcome! Use /help to see available commands.")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        help_text = (
            "Here are the commands you can use:\n\n"
            "/start - Start the bot and get a welcome message.\n"
            "/alert [symbol] [price] [below/above] - Set a price alert.\n"
            "/listalerts - List all your active alerts.\n"
            "/deletealert [id] - Delete an alert by its ID.\n"
            "/p [symbol] - Get the current price of a trading pair.\n"
            "/rsi [symbol] - Get the RSI (Relative Strength Index) for a trading pair.\n"
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
            add_alert(conn, message.from_user.id, symbol.upper(), price, condition.lower())
            bot.reply_to(message, f"Alert set for {symbol.upper()} at {price} ({condition.lower()}).")
        except ValueError:
            bot.reply_to(message, "Invalid command format. Use /alert [symbol] [price] [below/above].")

    @bot.message_handler(commands=['listalerts'])
    def handle_list_alerts(message):
        alerts = list_alerts(conn, message.from_user.id)
        if alerts:
            response = "Your alerts:\n" + "\n".join([f"{id}: {symbol} at {price}" for id, symbol, price in alerts])
        else:
            response = "No active alerts."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['deletealert'])
    def handle_delete_alert(message):
        try:
            _, alert_id = message.text.split()
            delete_alert(conn, message.from_user.id, int(alert_id))
            bot.reply_to(message, "Alert deleted.")
        except ValueError:
            bot.reply_to(message, "Invalid command format. Use /deletealert [id].")

    @bot.message_handler(commands=['p'])
    def get_price(message):
        try:
            _, symbol = message.text.split()
            price = fetch_price(symbol.upper())
            if price:
                bot.reply_to(message, f"Current price of {symbol.upper()}: {price}")
            else:
                bot.reply_to(message, f"Symbol {symbol.upper()} not found.")
        except Exception as e:
            bot.reply_to(message, f"Error fetching price: {str(e)}")

    @bot.message_handler(commands=['rsi'])
    def get_rsi(message):
        """
        Fetches the RSI for a given trading pair and responds to the user.
        """
        try:
            _, symbol = message.text.split()
            prices = fetch_historical_prices(symbol.upper(), interval='15', limit=100)

            if not prices:
                bot.reply_to(message, f"Unable to fetch historical data for {symbol.upper()}.")
                return

            rsi = calculate_rsi(prices)
            bot.reply_to(message, f"RSI for {symbol.upper()} (15-min interval): {rsi:.2f}")
        except ValueError:
            bot.reply_to(message, "Invalid command format. Use /rsi [symbol].")
        except Exception as e:
            bot.reply_to(message, f"Error calculating RSI: {str(e)}")

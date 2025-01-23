# File: bybit_alert_bot/main.py

from telebot import TeleBot
from config import API_TOKEN
from bot.commands import register_commands
from bot.price_tracking import start_price_tracking
from db.db_operations import initialize_database, get_connection

# Initialize the database
initialize_database()

# Create a database connection
conn = get_connection()

# Initialize the bot
bot = TeleBot(API_TOKEN)

def main():
    # Register bot commands
    register_commands(bot, conn)

    # Start price tracking in a background thread
    start_price_tracking(bot, conn)

    # Start polling for bot messages
    print("Bot is running...")
    bot.polling()

if __name__ == "__main__":
    main()

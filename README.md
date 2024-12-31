Here’s a `README.md` file for your Bybit Alert Bot project:

```markdown
# Bybit Alert Bot

Bybit Alert Bot is a Telegram bot that allows users to set price alerts for cryptocurrency trading pairs on Bybit. Users can set alerts for when the price drops below or rises above a specified threshold. The bot fetches real-time data from the Bybit API and notifies users when their alert conditions are met.

## Features

- **Set Alerts**: Create alerts for price drops or rises.
- **Real-Time Monitoring**: Tracks cryptocurrency prices in the `linear` market category of Bybit.
- **List Alerts**: View all active alerts.
- **Delete Alerts**: Remove alerts by their ID.
- **Check Prices**: Get the current price of a trading pair.

## Commands

- `/start` - Start the bot and get a welcome message.
- `/alert [symbol] [price] [below/above]` - Set a price alert. Example: `/alert BTC 30000 below`.
- `/listalerts` - List all active alerts.
- `/deletealert [id]` - Delete an alert by its ID.
- `/p [symbol]` - Get the current price of a trading pair. Example: `/p BTC`.
- `/stop` - Stop the bot.
- `/help` - Show the help message.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kdkiss/crypto-alert-bot.git
   cd crypto-alert-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.py` file for your bot token:
   ```python
   # config.py
   API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
   ```

4. (Optional) Use environment variables for the token:
   ```python
   import os
   API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
   ```

   Set the environment variable:
   - **Linux/Mac**:
     ```bash
     export TELEGRAM_BOT_TOKEN='YOUR_TELEGRAM_BOT_API_TOKEN'
     ```
   - **Windows**:
     ```cmd
     set TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_API_TOKEN
     ```

5. Initialize the SQLite database:
   ```bash
   python
   >>> import sqlite3
   >>> conn = sqlite3.connect('alerts.db')
   >>> cursor = conn.cursor()
   >>> cursor.execute('''
       CREATE TABLE IF NOT EXISTS alerts (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           user_id INTEGER NOT NULL,
           symbol TEXT NOT NULL,
           price REAL NOT NULL,
           condition TEXT NOT NULL
       )
   ''')
   >>> conn.commit()
   >>> conn.close()
   ```

6. Run the bot:
   ```bash
   python bybit_alert_bot.py
   ```

## Usage

### Setting an Alert
Use the `/alert` command to create an alert. Example:
```plaintext
/alert BTC 30000 below
```

This sets an alert for when BTC drops below $30,000.

### Listing Alerts
View all your active alerts:
```plaintext
/listalerts
```

### Deleting Alerts
Remove an alert by its ID:
```plaintext
/deletealert 1
```

### Checking Prices
Get the current price of a trading pair:
```plaintext
/p BTC
```

## Environment Setup

- **Python Version**: Python 3.8 or later.
- **Dependencies**:
  - `pyTelegramBotAPI`
  - `requests`
  - `sqlite3`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Deployment

1. **Host Locally**: Run the bot using `python`.
2. **Deploy on a Server**:
   - Use platforms like AWS, DigitalOcean, or Heroku.
   - Set up environment variables for secure token storage.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [Bybit API](https://bybit.com).
- Built using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
```

---
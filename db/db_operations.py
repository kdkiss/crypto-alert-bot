# File: bybit_alert_bot/db/db_operations.py

import sqlite3

DB_PATH = 'alerts.db'

def initialize_database():
    """
    Initializes the database by creating the necessary tables.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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
    conn.close()

def get_connection():
    """
    Creates and returns a connection to the database.
    :return: SQLite database connection.
    """
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def add_alert(conn, user_id, symbol, price, condition):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO alerts (user_id, symbol, price, condition) VALUES (?, ?, ?, ?)',
        (user_id, symbol, price, condition)
    )
    conn.commit()

def list_alerts(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT id, symbol, price FROM alerts WHERE user_id = ?', (user_id,))
    return cursor.fetchall()

def remove_alert(cursor, conn, alert_id):
    cursor.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
    conn.commit()

def get_alerts(cursor):
    cursor.execute('SELECT id, user_id, symbol, price, condition FROM alerts')
    return cursor.fetchall()

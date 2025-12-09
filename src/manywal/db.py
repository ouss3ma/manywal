import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent.parent / "data" / "manywal.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    """Initialize the database with users and transactions tables."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                shop TEXT,
                category TEXT,
                transaction_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)

            conn.commit()
            logger.info(f"Database initialized successfully at {DB_PATH}")
            return True
    except sqlite3.Error as e:
        logger.error(f"SQLite error during DB initialization: {e}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error during DB initialization: {e}")
        return False

def db_insert_user(name: str) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username) VALUES (?)",
            (name,)
        )
        connection.commit()

def db_select_users() -> list:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT username from users"
        )
        users = cursor.fetchall()
        return [user[0] for user in users] 

def db_select_user_id(username: str) -> int | None:
    """Return user_id for a username or None."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else None

def db_insert_transaction(user_id: int, amount: float, shop: str, category: str, transaction_date: str) -> int:
    """Insert a transaction row. Returns True on success."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (user_id, amount, shop, category, transaction_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, shop, category, transaction_date)
        )
        conn.commit()
        return cursor.lastrowid

def db_select_transactions(user_id: int, start_date: str, end_date: str) -> list:
    """Return all transactions for a user between start_date and end_date."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT amount, shop, category, transaction_date
            FROM transactions
            WHERE user_id = ? AND transaction_date BETWEEN ? AND ?
            ORDER BY transaction_date ASC
            """,
            (user_id, start_date, end_date)
        )
        transactions = cursor.fetchall()
        return transactions

if __name__ == "__main__":
    init_db()
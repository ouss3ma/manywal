import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
DB_PATH = Path(__file__).parent.parent.parent / "data" / "manywal.db"

def insert_user(name: str) -> None:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username) VALUES (?)",
        (name,)
    )
    connection.commit()

def select_users() -> list:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT username from users"
        )
        users = cursor.fetchall()
        return [user[0] for user in users] 

def get_user_id(username: str) -> int | None:
    """Return user_id for a username or None."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else None

def insert_transaction(user_id: int, amount: float, shop: str, category: str, transaction_date: str) -> int:
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

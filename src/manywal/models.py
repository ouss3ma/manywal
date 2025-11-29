import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
DB_PATH = Path(__file__).parent.parent.parent / "data" / "manywal.db"

def insert_user(name: str) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username) VALUES (?)",
            (name,)
        )
        connection.commit()

def select_users() -> list:
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT username from users"
            )
            users = cursor.fetchall()
            return [user[0] for user in users]
    except sqlite3.Error as e:
        logger.error(f"Database error while selecting users: {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return []


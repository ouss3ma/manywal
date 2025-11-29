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
    except sqlite3.Error as e:
        logger.error(f"SQLite error during DB initialization: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error during DB initialization: {e}")

if __name__ == "__main__":
    init_db()
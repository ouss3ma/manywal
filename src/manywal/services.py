import sqlite3
import logging
import re
import typer
from . import db
from . import utils

USERNAME_RE = re.compile(r"^[A-Za-z]+$")

logger = logging.getLogger(__name__)

def db_add_user(name:str) -> bool:
    try:
        if not USERNAME_RE.match(name):
            typer.echo("Username must contain only alphabetic characters.")
            return False
        else:
            db.insert_user(name)
            return True
    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return False

def db_list_users() -> list | None:
    try:
        return db.select_users()
    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return None

def db_add_transaction(username: str, amount:float, shop: str, category: str, transaction_date:str) -> None:
    try:
        user_id = db.get_user_id(username)
        if not utils.validate_date(transaction_date):
            logger.error(f"Invalid date format: {transaction_date}. Use YYYY-MM-DD.")
            return False
        if user_id is None:
            logger.error(f"Unknown user: {username}")
            return False
        t_id = db.insert_transaction(user_id, amount, shop, category, transaction_date)
        logger.info(f"Transaction {t_id} added for {username}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    
def db_get_transactions(username: str, start_date:str, end_date:str) -> None:
    try:
        user_id = db.get_user_id(username)
        if not utils.validate_date(start_date):
            logger.error(f"Invalid date format: {start_date}. Use YYYY-MM-DD.")
            return False
        if not utils.validate_date(end_date):
            logger.error(f"Invalid date format: {end_date}. Use YYYY-MM-DD.")
            return False
        if user_id is None:
            logger.error(f"Unknown user: {username}")
            return False
        return db.select_transaction(user_id, start_date, end_date)
    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
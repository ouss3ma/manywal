from .models import insert_user, select_users

def db_add_user(name:str) -> bool:
    if name is None:
        raise ValueError("user name cannot be empty")
        return False
    try:
        insert_user(name)
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return False

def db_list_users() -> list | None:
    try:
        return select_users()
    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return None

def db_add_transaction(username: str, amount:float, shop: str, category: str, transaction_date:str) -> None:
    try:
        user_id = get_user_id(username)
        if user_id is None:
            logger.warning(f"Unknown user: {username}")
            return False
        t_id = insert_transaction(user_id, amount, shop, category, date)
        logger.info(f"Transaction {t_id} added for {username}")
        return True

    except sqlite3.Error as e:
        logger.error(f"Database error while adding transaction: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    
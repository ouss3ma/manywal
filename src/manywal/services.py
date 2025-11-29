from .models import insert_user, select_users

def db_add_user(name:str) -> None:
    if name is None:
        raise ValueError("user name cannot be empty")
    insert_user(name)

def db_list_users() -> list:
    return select_users()
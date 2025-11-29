import typer
from .services import db_add_user, db_list_users
from .logging_setup import setup_logging

logger = setup_logging()

app = typer.Typer(help="ManyWal CLI - A tool for managing your wallet.")

@app.command()
def add_user(name: str):
    """Add a user"""
    db_add_user(name)
    logger.info("user added")

@app.command()
def get_list_users():
    """Get list of all users"""
    for user in db_list_users():
        typer.echo(user)

def main():
    app()

if __name__ == "__main__":
    main()
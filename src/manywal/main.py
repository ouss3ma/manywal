import typer
from rich.table import Table
from rich.console import Console
from .services import *
from .logging_setup import setup_logging
from .db import init_db

logger = setup_logging()
console = Console()

app = typer.Typer(help="ManyWal CLI - A tool for managing your wallet.")

@app.command()
def create_db():
    """create db and tables"""
    init_db()
    logger.info("db and tables created")

@app.command()
def add_user(name: str):
    """Add a user"""
    if create_user(name):
        logger.info("user added")

@app.command()
def get_user_list():
    """Get list of all users"""
    rows = list_users()
    if not rows:
        console.print("[red]No users found.[/red]")
        raise typer.Exit()
    table = Table(title=f"List of Users")
    table.add_column("Username")
    for r in rows:
        table.add_row(r)
    console.print(table)

@app.command()
def add_transaction(username: str, amount:float, shop: str, category: str, transaction_date:str):
    """Insert a new transaction"""
    if create_transaction(username, amount, shop, category, transaction_date):
        logger.info("transaction added")

@app.command()
def get_transaction_list(username: str, start_date:str, end_date:str):
    """get all transactions for a user  between start_date and end_date"""
    rows = list_transactions(username, start_date, end_date)
    if not rows:
        console.print("[red]No transactions found.[/red]")
        raise typer.Exit()
    table = Table(title=f"Transactions for {username}")
    table.add_column("Amount")
    table.add_column("Shop")
    table.add_column("Category")
    table.add_column("Date")

    for r in rows:
        table.add_row(*[str(x) for x in r])

    console.print(table)

def main():
    app()

if __name__ == "__main__":
    main()
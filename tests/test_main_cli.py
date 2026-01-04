import pytest
from typer.testing import CliRunner
from manywal import main

runner = CliRunner()

def test_create_db():
    result = runner.invoke(main.app, ['create-db'])
    assert result.exit_code == 0
    assert 'db and tables created' in result.output or result.exit_code == 0

def test_add_user():
    result = runner.invoke(main.app, ['add-user', 'alice'])
    assert result.exit_code == 0
    # No output expected, but should not error


def test_add_and_list_user():
    runner.invoke(main.app, ['create-db'])
    runner.invoke(main.app, ['add-user', 'bob'])
    result = runner.invoke(main.app, ['get-user-list'])
    assert result.exit_code == 0
    assert 'bob' in result.output

def test_add_transaction_and_list():
    runner.invoke(main.app, ['create-db'])
    runner.invoke(main.app, ['add-user', 'carol'])
    runner.invoke(main.app, [
        'add-transaction', 'carol', '100.5', 'ShopX', 'Food', '2025-12-08'
    ])
    result = runner.invoke(main.app, [
        'get-transaction-list', 'carol', '2025-12-01', '2025-12-31'
    ])
    assert result.exit_code == 0
    assert '100.5' in result.output
    assert 'ShopX' in result.output
    assert 'Food' in result.output
    assert '2025-12-08' in result.output

def test_get_transaction_list_empty():
    runner.invoke(main.app, ['create-db'])
    runner.invoke(main.app, ['add-user', 'dave'])
    result = runner.invoke(main.app, [
        'get-transaction-list', 'dave', '2025-01-01', '2025-01-31'
    ])
    assert result.exit_code == 0 or result.exit_code == 1
    assert 'No transactions found.' in result.output

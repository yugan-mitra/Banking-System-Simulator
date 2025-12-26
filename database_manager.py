"""
Database Manager Module

Handles all database operations for the banking system including
saving and loading account data from CSV files.
"""

import csv
from pathlib import Path

from accounts import (
    BankAccount,
    SavingsAccount,
    CreditAccount,
    MASTER_FILE,
    MASTER_HEADERS,
    ACCOUNT_TYPE_SAVINGS,
    ACCOUNT_TYPE_CREDIT
)


def save_master_data(accounts: list[BankAccount]) -> bool:
    """
    Save all account data to the master CSV file.
    
    Args:
        accounts: List of all bank accounts to save.
        
    Returns:
        True if save was successful, False otherwise.
    """
    try:
        with open(MASTER_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(MASTER_HEADERS)

            for account in accounts:
                row = _account_to_row(account)
                if row:
                    writer.writerow(row)
        return True
    except OSError as error:
        print(f"⚠️ Error saving master data: {error}")
        return False


def _account_to_row(account: BankAccount) -> list | None:
    """
    Convert a bank account to a CSV row.
    
    Args:
        account: The account to convert.
        
    Returns:
        List representing the CSV row, or None if account type is unknown.
    """
    if isinstance(account, SavingsAccount):
        return [
            ACCOUNT_TYPE_SAVINGS,
            account.account_number,
            account.holder_name,
            f"{account.get_balance():.2f}",
            account.interest_rate,
            account.min_balance
        ]
    elif isinstance(account, CreditAccount):
        return [
            ACCOUNT_TYPE_CREDIT,
            account.account_number,
            account.holder_name,
            f"{account.get_balance():.2f}",
            account.credit_limit,
            "N/A"
        ]
    return None


def load_master_data() -> list[BankAccount]:
    """
    Load all accounts from the master CSV file.
    
    Returns:
        List of loaded bank accounts.
    """
    if not MASTER_FILE.exists():
        return []

    accounts: list[BankAccount] = []
    
    try:
        with open(MASTER_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row

            for row in reader:
                account = _row_to_account(row)
                if account:
                    accounts.append(account)

    except (ValueError, OSError) as error:
        print(f"⚠️ Error loading master file: {error}")

    return accounts


def _row_to_account(row: list[str]) -> BankAccount | None:
    """
    Convert a CSV row to a bank account object.
    
    Args:
        row: CSV row data.
        
    Returns:
        BankAccount instance or None if row is invalid.
    """
    if not row or len(row) < 5:
        return None

    try:
        account_type = row[0]
        account_number = int(row[1])
        holder_name = row[2]
        balance = float(row[3])

        if account_type == ACCOUNT_TYPE_SAVINGS:
            return SavingsAccount(
                holder_name=holder_name,
                initial_balance=balance,
                account_number=account_number,
                interest_rate=float(row[4]),
                min_balance=float(row[5])
            )
        elif account_type == ACCOUNT_TYPE_CREDIT:
            return CreditAccount(
                holder_name=holder_name,
                initial_balance=balance,
                account_number=account_number,
                credit_limit=float(row[4])
            )
    except (ValueError, IndexError):
        pass

    return None

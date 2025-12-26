"""
Accounts Package

This package contains all account types for the banking system.

Classes:
    BankAccount: Abstract base class for all account types.
    SavingsAccount: Savings account with interest.
    CreditAccount: Credit account with credit limit.
"""

from .base_account import BankAccount
from .savings_account import SavingsAccount
from .credit_account import CreditAccount
from .constants import (
    DB_ROOT,
    MASTER_FILE,
    RECORDS_ROOT,
    SAVING_DIR,
    CREDIT_DIR,
    TRANSACTION_HEADERS,
    DATE_FORMAT,
    TIME_FORMAT,
    CURRENCY_PRECISION,
    MAX_INPUT_ATTEMPTS,
    MAX_TRANSACTION_ATTEMPTS,
    MIN_SAVINGS_DEPOSIT,
    MIN_CREDIT_DEPOSIT,
    MASTER_HEADERS,
    ACCOUNT_TYPE_SAVINGS,
    ACCOUNT_TYPE_CREDIT
)

__all__ = [
    "BankAccount",
    "SavingsAccount",
    "CreditAccount",
    "DB_ROOT",
    "MASTER_FILE",
    "RECORDS_ROOT",
    "SAVING_DIR",
    "CREDIT_DIR",
    "TRANSACTION_HEADERS",
    "DATE_FORMAT",
    "TIME_FORMAT",
    "CURRENCY_PRECISION",
    "MAX_INPUT_ATTEMPTS",
    "MAX_TRANSACTION_ATTEMPTS",
    "MIN_SAVINGS_DEPOSIT",
    "MIN_CREDIT_DEPOSIT",
    "MASTER_HEADERS",
    "ACCOUNT_TYPE_SAVINGS",
    "ACCOUNT_TYPE_CREDIT"
]

__version__ = "1.0.0"

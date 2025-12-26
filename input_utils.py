"""
Input Utilities Module

Provides input validation and helper functions for user interactions.
"""

from typing import Any

from accounts import BankAccount, MAX_INPUT_ATTEMPTS


def get_valid_input(prompt: str, data_type: type[Any]) -> Any:
    """
    Get validated user input with retry logic.
    
    Args:
        prompt: Input prompt to display.
        data_type: Expected data type for conversion.
        
    Returns:
        Converted value or None if all attempts fail.
    """
    for _ in range(MAX_INPUT_ATTEMPTS):
        try:
            user_input = input(prompt)
            return data_type(user_input)
        except ValueError:
            print("⚠️ Invalid format!")
    return None


def find_account(accounts: list[BankAccount]) -> BankAccount | None:
    """
    Find an account by account number.
    
    Args:
        accounts: List of accounts to search.
        
    Returns:
        Found account or None.
    """
    account_number = get_valid_input("Enter Account Number: ", int)
    
    if account_number is None:
        return None

    for account in accounts:
        if account.account_number == account_number:
            return account

    print("❌ Account not found.")
    return None

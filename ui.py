"""
User Interface Module

Handles menu display and user interaction flow.
"""

from accounts import BankAccount
from account_operations import (
    create_account,
    perform_transaction,
    transfer_money,
    display_all_accounts,
    end_of_month_process
)


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== 🏦 BANKING SYSTEM SIMULATOR ===")
    print("1. Open Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer Money")
    print("5. Show All Accounts")
    print("6. Month-End Process")
    print("7. Exit")


def handle_menu_choice(choice: str, accounts: list[BankAccount]) -> bool:
    """
    Handle the user's menu selection.
    
    Args:
        choice: User's menu choice.
        accounts: List of all accounts.
        
    Returns:
        False if user chose to exit, True otherwise.
    """
    menu_actions = {
        "1": lambda: create_account(accounts),
        "2": lambda: perform_transaction(accounts, "deposit"),
        "3": lambda: perform_transaction(accounts, "withdraw"),
        "4": lambda: transfer_money(accounts),
        "5": lambda: display_all_accounts(accounts),
        "6": lambda: end_of_month_process(accounts),
    }

    if choice == "7":
        print("Goodbye! 👋")
        return False

    action = menu_actions.get(choice)
    if action:
        action()
    else:
        print("Invalid option.")
    
    return True

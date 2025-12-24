from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Final

from accounts import SavingsAccount, CreditAccount, BankAccount

# =============================================================================
# Constants
# =============================================================================
DB_ROOT: Final[str] = "database"
MASTER_FILE: Final[Path] = Path(DB_ROOT) / "banking_master.csv"
RECORDS_ROOT: Final[Path] = Path(DB_ROOT) / "records"
SAVING_DIR: Final[Path] = RECORDS_ROOT / "saving"
CREDIT_DIR: Final[Path] = RECORDS_ROOT / "credit"

# Input validation
MAX_INPUT_ATTEMPTS: Final[int] = 3
MAX_TRANSACTION_ATTEMPTS: Final[int] = 3

# Minimum deposits
MIN_SAVINGS_DEPOSIT: Final[float] = 500.00
MIN_CREDIT_DEPOSIT: Final[float] = 5000.00

# Master file headers
MASTER_HEADERS: Final[tuple[str, ...]] = (
    "Type", "AccNum", "Name", "CurrentBalance", "Rate_Limit", "MinBal_Fee"
)

# Account type identifiers
ACCOUNT_TYPE_SAVINGS: Final[str] = "SAVINGS"
ACCOUNT_TYPE_CREDIT: Final[str] = "CREDIT"


# =============================================================================
# System Initialization
# =============================================================================
def initialize_system() -> None:
    """Create required database directories if they don't exist."""
    directories = [DB_ROOT, RECORDS_ROOT, SAVING_DIR, CREDIT_DIR]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


# =============================================================================
# Master Database Operations
# =============================================================================
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


# =============================================================================
# Input Helpers
# =============================================================================
def get_valid_input[T](prompt: str, data_type: type[T]) -> T | None:
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


# =============================================================================
# Menu Operations
# =============================================================================
def create_account(accounts: list[BankAccount]) -> None:
    """
    Create a new savings or credit account.
    
    Args:
        accounts: List to append the new account to.
    """
    print("\n--- Open New Account ---")

    # Display account type options
    print(f"1. Savings Account (Min Deposit: Rs. {MIN_SAVINGS_DEPOSIT:.0f})")
    print(f"2. Credit Account  (Min Deposit: Rs. {MIN_CREDIT_DEPOSIT:.0f})")
    
    account_type = get_valid_input("Select Account Type (1 or 2): ", int)
    
    if account_type not in (1, 2):
        print("❌ Invalid choice.")
        return

    # Get holder name
    holder_name = input("Enter Holder Name: ").strip()
    if not holder_name:
        print("❌ Holder name cannot be empty.")
        return

    # Get initial deposit
    initial_deposit = get_valid_input("Enter Initial Deposit Amount: ", float)
    if initial_deposit is None:
        return

    # Create account based on type
    new_account = _create_account_by_type(account_type, holder_name, initial_deposit)
    
    if new_account is None:
        return

    accounts.append(new_account)
    print(f"✅ Account Created Successfully! Number: {new_account.account_number}")
    save_master_data(accounts)


def _create_account_by_type(
    account_type: int, 
    holder_name: str, 
    initial_deposit: float
) -> BankAccount | None:
    """
    Create an account based on the selected type.
    
    Args:
        account_type: 1 for Savings, 2 for Credit.
        holder_name: Name of the account holder.
        initial_deposit: Initial deposit amount.
        
    Returns:
        Created account or None if validation fails.
    """
    if account_type == 1:  # Savings
        if initial_deposit < MIN_SAVINGS_DEPOSIT:
            print(f"❌ Error: Minimum initial deposit for Savings Account is Rs. {MIN_SAVINGS_DEPOSIT:.2f}")
            return None
        return SavingsAccount(holder_name, initial_deposit)
    
    elif account_type == 2:  # Credit
        if initial_deposit < MIN_CREDIT_DEPOSIT:
            print(f"❌ Error: Minimum initial deposit for Credit Account is Rs. {MIN_CREDIT_DEPOSIT:.2f}")
            return None
        return CreditAccount(holder_name, initial_deposit)
    
    return None


def perform_transaction(accounts: list[BankAccount], transaction_type: str) -> None:
    """
    Perform a deposit or withdrawal transaction.
    
    Args:
        accounts: List of all accounts.
        transaction_type: Either "deposit" or "withdraw".
    """
    account = find_account(accounts)
    if account is None:
        return

    print(f"Current Balance: Rs. {account.get_balance():.2f}")

    for attempt in range(1, MAX_TRANSACTION_ATTEMPTS + 1):
        amount = get_valid_input(f"Enter amount to {transaction_type}: ", float)

        if amount is None:
            _handle_failed_attempt(attempt, "Invalid input")
            if attempt == MAX_TRANSACTION_ATTEMPTS:
                return
            continue

        success = _execute_transaction(account, transaction_type, amount)

        if success:
            save_master_data(accounts)
            return

        _handle_failed_attempt(attempt, "Transaction failed")
        if attempt < MAX_TRANSACTION_ATTEMPTS:
            print(f"Current Balance: Rs. {account.get_balance():.2f}")


def _execute_transaction(
    account: BankAccount, 
    transaction_type: str, 
    amount: float
) -> bool:
    """
    Execute the actual transaction on the account.
    
    Args:
        account: Account to transact on.
        transaction_type: Type of transaction.
        amount: Transaction amount.
        
    Returns:
        True if successful, False otherwise.
    """
    if transaction_type == "deposit":
        return account.deposit(amount)
    elif transaction_type == "withdraw":
        return account.withdraw(amount)
    
    print("❌ Unknown transaction type.")
    return False


def _handle_failed_attempt(attempt: int, reason: str) -> None:
    """Display appropriate message for failed transaction attempt."""
    print(f"❌ {reason} (attempt {attempt}/{MAX_TRANSACTION_ATTEMPTS}).")
    
    if attempt == MAX_TRANSACTION_ATTEMPTS:
        print("❌ Maximum attempts reached. Returning to main menu.")


def display_all_accounts(accounts: list[BankAccount]) -> None:
    """Display all registered accounts."""
    print("\n--- Account Registry ---")
    
    if not accounts:
        print("No accounts found.")
        return
    
    for account in accounts:
        print(account)


def end_of_month_process(accounts: list[BankAccount]) -> None:
    """
    Apply monthly interest/charges to all accounts.
    
    Args:
        accounts: List of all accounts to process.
    """
    print("\n--- End of Month Processing ---")
    
    for account in accounts:
        if isinstance(account, SavingsAccount):
            account.apply_interest()
        elif isinstance(account, CreditAccount):
            account.apply_debt_interest()

    save_master_data(accounts)
    print("✅ All accounts updated and saved.")


# =============================================================================
# Main Menu
# =============================================================================
def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== 🏦 BANKING SYSTEM SIMULATOR ===")
    print("1. Open Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Show All Accounts")
    print("5. Month-End Process")
    print("6. Exit")


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
        "4": lambda: display_all_accounts(accounts),
        "5": lambda: end_of_month_process(accounts),
    }

    if choice == "6":
        print("Goodbye! 👋")
        return False

    action = menu_actions.get(choice)
    if action:
        action()
    else:
        print("Invalid option.")
    
    return True


def main() -> None:
    """Main entry point for the banking system simulator."""
    initialize_system()
    accounts = load_master_data()
    
    print(f"🔄 System Loaded: {len(accounts)} accounts found.")

    running = True
    while running:
        display_menu()
        choice = input("Select: ").strip()
        running = handle_menu_choice(choice, accounts)


if __name__ == "__main__":
    main()
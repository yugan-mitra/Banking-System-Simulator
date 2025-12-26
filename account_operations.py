"""
Account Operations Module

Contains all business logic for account operations including
creating accounts, performing transactions, and transfers.
"""

from accounts import (
    BankAccount,
    SavingsAccount,
    CreditAccount,
    MAX_TRANSACTION_ATTEMPTS,
    MIN_SAVINGS_DEPOSIT,
    MIN_CREDIT_DEPOSIT
)
from input_utils import get_valid_input, find_account
from database_manager import save_master_data


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


def transfer_money(accounts: list[BankAccount]) -> None:
    """
    Transfer money from one account to another.
    
    Args:
        accounts: List of all accounts.
    """
    print("\n--- Money Transfer ---")
    
    # Get source account
    print("From Account:")
    from_account = find_account(accounts)
    if from_account is None:
        return
    
    # Get destination account
    print("\nTo Account:")
    to_account = find_account(accounts)
    if to_account is None:
        return
    
    # Check if same account
    if from_account.account_number == to_account.account_number:
        print("❌ Cannot transfer to the same account.")
        return
    
    print(f"\nFrom: {from_account}")
    print(f"To: {to_account}")
    
    # Get transfer amount
    amount = get_valid_input("\nEnter amount to transfer: ", float)
    if amount is None:
        return
    
    if amount <= 0:
        print("❌ Transfer amount must be positive.")
        return
    
    # Perform transfer
    print(f"\nProcessing transfer of Rs. {amount:.2f}...")
    
    # Withdraw from source (skip fee for transfers)
    # For SavingsAccount, use skip_fee=True; other accounts ignore this parameter
    if isinstance(from_account, SavingsAccount):
        success = from_account.withdraw(amount, skip_fee=True)
    else:
        success = from_account.withdraw(amount)
    
    if not success:
        print("❌ Transfer failed. Withdrawal unsuccessful.")
        return
    
    # Deposit to destination
    if not to_account.deposit(amount):
        print("❌ Transfer failed. Deposit unsuccessful.")
        # Rollback: return money to source account
        from_account.deposit(amount)
        return
    
    print(f"✅ Transfer successful! Rs. {amount:.2f} transferred.")
    save_master_data(accounts)

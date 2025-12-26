import csv
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from .constants import (
    RECORDS_ROOT,
    TRANSACTION_HEADERS,
    DATE_FORMAT,
    TIME_FORMAT,
    CURRENCY_PRECISION
)


class BankAccount(ABC):
    """
    Abstract base class for all bank accounts.
    
    Manages account numbers, balance, and transaction logging.
    Each subclass maintains its own account number sequence.
    
    Attributes:
        holder_name: Name of the account holder.
        account_number: Unique account identifier.
        record_folder: Subdirectory for transaction records.
    """
    
    # Subclasses must define their own starting number
    _next_account_number: ClassVar[int]
    _account_number_prefix: ClassVar[int]  # Starting prefix for the account type

    def __init__(
        self,
        holder_name: str,
        initial_balance: float = 0.00,
        account_number: int | None = None,
        record_folder: str = "general"
    ) -> None:
        """
        Initialize a new bank account.
        
        Args:
            holder_name: Name of the account holder.
            initial_balance: Starting balance (default: 0.00).
            account_number: Existing account number for loading (optional).
            record_folder: Subdirectory name for transaction records.
        """
        self.holder_name = holder_name
        self._balance = float(initial_balance)
        self.record_folder = record_folder

        if account_number is not None:
            self.account_number = int(account_number)
            self._update_next_account_number()
        else:
            self.account_number = self._generate_account_number()
            self._log_transaction("Account Created", initial_balance)

    @classmethod
    def _generate_account_number(cls) -> int:
        """Generate and return the next available account number for this account type."""
        account_number = cls._next_account_number
        cls._next_account_number += 1
        return account_number

    def _update_next_account_number(self) -> None:
        """Update the class counter if loaded account number is higher."""
        if self.account_number >= type(self)._next_account_number:
            type(self)._next_account_number = self.account_number + 1

    def _log_transaction(self, transaction_type: str, amount: float) -> None:
        """
        Record a transaction to the account's CSV log file.
        
        Args:
            transaction_type: Description of the transaction.
            amount: Transaction amount (positive or negative).
        """
        folder_path = RECORDS_ROOT / self.record_folder
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / f"acc_{self.account_number}.csv"
        file_exists = file_path.is_file()

        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(TRANSACTION_HEADERS)

            now = datetime.now()
            writer.writerow([
                now.strftime(DATE_FORMAT),
                now.strftime(TIME_FORMAT),
                transaction_type,
                f"{amount:.{CURRENCY_PRECISION}f}",
                f"{self._balance:.{CURRENCY_PRECISION}f}"
            ])

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive).
            
        Returns:
            True if deposit was successful, False otherwise.
        """
        if amount <= 0:
            print("❌ Invalid deposit amount.")
            return False

        self._balance += amount
        print(f"✅ Deposited Rs. {amount:.2f}. New Balance: Rs. {self._balance:.2f}")
        self._log_transaction("Deposit", amount)
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw.
            
        Returns:
            True if withdrawal was successful, False otherwise.
        """
        if amount <= 0 or amount > self._balance:
            print("❌ Insufficient funds or invalid amount.")
            return False

        self._balance -= amount
        print(f"✅ Withdrew Rs. {amount:.2f}. New Balance: Rs. {self._balance:.2f}")
        self._log_transaction("Withdrawal", -amount)
        return True

    def get_balance(self) -> float:
        """Get the current account balance (legacy method)."""
        return self._balance

    def _set_balance(self, new_balance: float) -> None:
        """Set a new balance (for internal use only)."""
        self._balance = new_balance

    def __str__(self) -> str:
        """Return a string representation of the account."""
        return f"[Acc: {self.account_number}] {self.holder_name} : Rs. {self._balance:.2f}"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"holder_name={self.holder_name!r}, "
            f"balance={self._balance:.2f}, "
            f"account_number={self.account_number})"
        )

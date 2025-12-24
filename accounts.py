from __future__ import annotations

import csv
import os
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Final

# =============================================================================
# Constants
# =============================================================================
DB_ROOT: Final[str] = "database"
RECORDS_ROOT: Final[Path] = Path(DB_ROOT) / "records"

# Transaction Log Headers
TRANSACTION_HEADERS: Final[tuple[str, ...]] = (
    "Date", "Time", "Transaction", "Amount", "New Balance"
)

# Date/Time Formats
DATE_FORMAT: Final[str] = "%Y-%m-%d"
TIME_FORMAT: Final[str] = "%H:%M:%S"

# Decimal Places for Currency
CURRENCY_PRECISION: Final[int] = 2


# =============================================================================
# Base Account Class
# =============================================================================
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

    @classmethod
    def _update_next_account_number(cls) -> None:
        """Update the class counter if loaded account number is higher."""
        # This will be called by subclass with proper cls reference
        pass
    
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

    @property
    def balance(self) -> float:
        """Get the current account balance."""
        return self._balance

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


# =============================================================================
# Savings Account Class
# =============================================================================
class SavingsAccount(BankAccount):
    """
    Savings account with interest and minimum balance requirements.
    
    Account numbers start from 1200.
    
    Attributes:
        interest_rate: Annual interest rate (default: 4%).
        min_balance: Minimum balance to maintain (default: Rs. 500).
    """
    
    # Account number sequence for Savings accounts (starts at 1200)
    _account_number_prefix: ClassVar[int] = 1200
    _next_account_number: ClassVar[int] = 1200
    
    # Class-level constants
    MIN_WITHDRAWAL_AMOUNT: ClassVar[float] = 50.00
    DEFAULT_INTEREST_RATE: ClassVar[float] = 0.04
    DEFAULT_MIN_BALANCE: ClassVar[float] = 500.00
    MONTHS_PER_YEAR: ClassVar[int] = 12

    def __init__(
        self,
        holder_name: str,
        initial_balance: float = 0.00,
        account_number: int | None = None,
        interest_rate: float = DEFAULT_INTEREST_RATE,
        min_balance: float = DEFAULT_MIN_BALANCE
    ) -> None:
        """
        Initialize a savings account.
        
        Args:
            holder_name: Name of the account holder.
            initial_balance: Starting balance.
            account_number: Existing account number (for loading).
            interest_rate: Annual interest rate.
            min_balance: Minimum balance requirement.
        """
        super().__init__(holder_name, initial_balance, account_number, record_folder="saving")
        self.interest_rate = float(interest_rate)
        self.min_balance = float(min_balance)

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw from savings with minimum amount and balance checks.
        
        Args:
            amount: Amount to withdraw.
            
        Returns:
            True if withdrawal was successful, False otherwise.
        """
        # Check minimum withdrawal amount
        if amount < self.MIN_WITHDRAWAL_AMOUNT:
            print(f"❌ Transaction Failed! Minimum withdrawal amount is Rs. {self.MIN_WITHDRAWAL_AMOUNT:.2f}")
            return False

        # Check minimum balance maintenance
        if (self._balance - amount) < self.min_balance:
            print(f"❌ Transaction Failed! You must maintain a minimum balance of Rs. {self.min_balance:.2f}")
            return False

        return super().withdraw(amount)

    def apply_interest(self) -> None:
        """Apply monthly interest to the account balance."""
        monthly_rate = self.interest_rate / self.MONTHS_PER_YEAR
        interest_amount = self._balance * monthly_rate
        self.deposit(interest_amount)
        print("💰 Monthly Interest applied.")


# =============================================================================
# Credit Account Class
# =============================================================================
class CreditAccount(BankAccount):
    """
    Credit account with credit limit and cash advance features.
    
    Account numbers start from 1900.
    
    Attributes:
        credit_limit: Maximum credit available.
        debt_interest_rate: Annual interest rate on debt.
        cash_advance_fee: Percentage fee for cash withdrawals.
    """
    
    # Account number sequence for Credit accounts (starts at 1900)
    _account_number_prefix: ClassVar[int] = 1900
    _next_account_number: ClassVar[int] = 1900
    
    # Class-level constants
    MIN_CASH_ADVANCE_AMOUNT: ClassVar[float] = 500.00
    DEFAULT_CREDIT_LIMIT: ClassVar[float] = 5000.00
    DEFAULT_DEBT_INTEREST_RATE: ClassVar[float] = 0.15
    DEFAULT_CASH_ADVANCE_FEE: ClassVar[float] = 0.03
    MONTHS_PER_YEAR: ClassVar[int] = 12

    def __init__(
        self,
        holder_name: str,
        initial_balance: float = 0.00,
        account_number: int | None = None,
        credit_limit: float = DEFAULT_CREDIT_LIMIT,
        debt_interest_rate: float = DEFAULT_DEBT_INTEREST_RATE,
        cash_advance_fee: float = DEFAULT_CASH_ADVANCE_FEE
    ) -> None:
        """
        Initialize a credit account.
        
        Args:
            holder_name: Name of the account holder.
            initial_balance: Starting balance.
            account_number: Existing account number (for loading).
            credit_limit: Maximum credit limit.
            debt_interest_rate: Annual interest rate on debt.
            cash_advance_fee: Fee percentage for cash advances.
        """
        super().__init__(holder_name, initial_balance, account_number, record_folder="credit")
        self.credit_limit = float(credit_limit)
        self.debt_interest_rate = float(debt_interest_rate)
        self.cash_advance_fee = float(cash_advance_fee)

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw cash with credit limit check and cash advance fee.
        
        Args:
            amount: Amount to withdraw.
            
        Returns:
            True if withdrawal was successful, False otherwise.
        """
        # Check minimum cash advance amount
        if amount < self.MIN_CASH_ADVANCE_AMOUNT:
            print(f"❌ Transaction Failed! Minimum Cash Advance amount is Rs. {self.MIN_CASH_ADVANCE_AMOUNT:.2f}")
            return False

        fee = amount * self.cash_advance_fee
        total_cost = amount + fee

        # Check credit limit
        if (self._balance - total_cost) < -self.credit_limit:
            print(f"❌ Limit Exceeded. Available Credit: Rs. {self.available_credit:.2f}")
            return False

        # Process withdrawal
        self._balance -= amount
        self._log_transaction("Withdrawal", -amount)

        # Apply cash advance fee
        self._balance -= fee
        self._log_transaction("Cash Advance Fee", -fee)

        print(f"✅ Withdrew Rs. {amount:.2f} (Fee: Rs. {fee:.2f}). New Balance: Rs. {self._balance:.2f}")
        return True

    def apply_debt_interest(self) -> None:
        """Apply monthly interest on outstanding debt (negative balance)."""
        if self._balance >= 0:
            return

        monthly_rate = self.debt_interest_rate / self.MONTHS_PER_YEAR
        interest_amount = abs(self._balance) * monthly_rate
        
        self._balance -= interest_amount
        print(f"📉 Debt Interest Charged: Rs. {interest_amount:.2f}")
        self._log_transaction("Debt Interest Charge", -interest_amount)

    @property
    def available_credit(self) -> float:
        """Get the remaining available credit."""
        return self.credit_limit + self._balance

    def get_available_credit(self) -> float:
        """Get available credit (legacy method)."""
        return self.available_credit
from typing import ClassVar

from .base_account import BankAccount


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
    WITHDRAWAL_FEE: ClassVar[float] = 5.00
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

    def withdraw(self, amount: float, skip_fee: bool = False) -> bool:
        """
        Withdraw from savings with minimum amount and balance checks.
        Also applies a Rs.5 withdrawal fee for regular withdrawals (not transfers).
        
        Args:
            amount: Amount to withdraw.
            skip_fee: If True, skip the withdrawal fee (used for transfers).
            
        Returns:
            True if withdrawal was successful, False otherwise.
        """
        # Check minimum withdrawal amount
        if amount < self.MIN_WITHDRAWAL_AMOUNT:
            print(f"❌ Transaction Failed! Minimum withdrawal amount is Rs. {self.MIN_WITHDRAWAL_AMOUNT:.2f}")
            return False

        # Check minimum balance maintenance (including fee if applicable)
        fee_amount = 0 if skip_fee else self.WITHDRAWAL_FEE
        total_deduction = amount + fee_amount
        if (self._balance - total_deduction) < self.min_balance:
            print(f"❌ Transaction Failed! You must maintain a minimum balance of Rs. {self.min_balance:.2f}")
            if not skip_fee:
                print(f"   (Note: Rs. {self.WITHDRAWAL_FEE:.2f} withdrawal fee applies)")
            return False

        # Perform withdrawal
        success = super().withdraw(amount)
        
        if success and not skip_fee:
            # Apply withdrawal fee only for regular withdrawals
            self._balance -= self.WITHDRAWAL_FEE
            self._log_transaction("Withdrawal Fee", -self.WITHDRAWAL_FEE)
            print(f"💳 Withdrawal fee of Rs. {self.WITHDRAWAL_FEE:.2f} applied.")
        
        return success

    def apply_interest(self) -> None:
        """Apply monthly interest to the account balance."""
        monthly_rate = self.interest_rate / self.MONTHS_PER_YEAR
        interest_amount = self._balance * monthly_rate
        self.deposit(interest_amount)
        print("💰 Monthly Interest applied.")

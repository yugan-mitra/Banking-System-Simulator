from typing import ClassVar

from .base_account import BankAccount


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

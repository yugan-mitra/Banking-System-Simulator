import csv
import os
import datetime

# Database Paths
DB_ROOT = 'database'
RECORDS_ROOT = os.path.join(DB_ROOT, 'records')

class BankAccount:
    # Base Class: Manages account numbers, balance, and transaction logging.
    next_acc_num = 1000 

    def __init__(self, holder_name, initial_balance=0.00, account_number=None, record_folder="general"):
        self.holder_name = holder_name
        self.__balance = float(initial_balance)
        self.record_folder = record_folder 

        if account_number is not None:
            self.account_number = int(account_number)
            if self.account_number >= BankAccount.next_acc_num:
                BankAccount.next_acc_num = self.account_number + 1
        else:
            self.account_number = BankAccount.next_acc_num
            BankAccount.next_acc_num += 1
            self.log_transaction("Account Created", initial_balance)

    def log_transaction(self, trans_type, amount):
        # Saves transaction to CSV.
        folder_path = os.path.join(RECORDS_ROOT, self.record_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = os.path.join(folder_path, f"acc_{self.account_number}.csv")
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Date', 'Time', 'Transaction', 'Amount', 'New Balance'])
            
            now = datetime.datetime.now()
            writer.writerow([
                now.strftime("%Y-%m-%d"), 
                now.strftime("%H:%M:%S"), 
                trans_type, 
                f"{amount:.2f}", # Store with 2 decimal places
                f"{self.__balance:.2f}"
            ])

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"✅ Deposited Rs. {amount:.2f}. New Balance: Rs. {self.__balance:.2f}")
            self.log_transaction("Deposit", amount)
            return True
        else:
            print("❌ Invalid deposit amount.")
            return False

    def withdraw(self, amount):
        # Base withdrawal logic
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"✅ Withdrew Rs. {amount:.2f}. New Balance: Rs. {self.__balance:.2f}")
            self.log_transaction("Withdrawal", -amount)
            return True
        else:
            print("❌ Insufficient funds or invalid amount.")
            return False

    def get_balance(self):
        return self.__balance
    
    def _set_balance(self, new_balance):
        self.__balance = new_balance

    def __str__(self):
        return f"[Acc: {self.account_number}] {self.holder_name} : Rs. {self.__balance:.2f}"


class SavingsAccount(BankAccount):
    def __init__(self, holder_name, initial_balance=0.00, account_number=None, interest_rate=0.04, min_balance=500.00):
        super().__init__(holder_name, initial_balance, account_number, record_folder="saving")
        self.interest_rate = float(interest_rate)
        self.min_balance = float(min_balance)

    def withdraw(self, amount):
        # 1. Minimum Withdrawal Limit Check
        if amount < 50.00:
            print("❌ Transaction Failed! Minimum withdrawal amount is Rs. 50.00")
            return False

        # 2. Minimum Balance Maintenance Check
        current_balance = self.get_balance()
        if (current_balance - amount) >= self.min_balance:
            return super().withdraw(amount)
        else:
            print(f"❌ Transaction Failed! You must maintain a minimum balance of Rs. {self.min_balance:.2f}")
            return False

    def apply_interest(self):
        monthly_rate = self.interest_rate / 12
        interest_amount = self.get_balance() * monthly_rate
        self.deposit(interest_amount)
        print(f"💰 Monthly Interest applied.")


class CreditAccount(BankAccount):
    def __init__(self, holder_name, initial_balance=0.00, account_number=None, credit_limit=5000.00, debt_interest_rate=0.15, cash_advance_fee=0.03):
        super().__init__(holder_name, initial_balance, account_number, record_folder="credit")
        self.credit_limit = float(credit_limit)
        self.debt_interest_rate = float(debt_interest_rate)
        self.cash_advance_fee = float(cash_advance_fee)

    def withdraw(self, amount):
        # 1. Real-world Check: Cash Advance Minimum
        if amount < 500.00:
            print("❌ Transaction Failed! Minimum Cash Advance amount is Rs. 500.00")
            return False

        fee = amount * self.cash_advance_fee
        total_cost = amount + fee
        
        # 2. Credit Limit Check
        if (self.get_balance() - total_cost) >= -self.credit_limit:
            new_bal = self.get_balance() - total_cost
            self._set_balance(new_bal)
            
            print(f"✅ Withdrew Rs. {amount:.2f} (Fee: Rs. {fee:.2f}). New Balance: Rs. {new_bal:.2f}")
            self.log_transaction(f"Withdrawal (+Fee Rs. {fee:.2f})", -total_cost)
            return True
        else:
            print(f"❌ Limit Exceeded. Available Credit: Rs. {self.get_available_credit():.2f}")
            return False

    def apply_debt_interest(self):
        current_balance = self.get_balance()
        if current_balance < 0.00:
            monthly_rate = self.debt_interest_rate / 12
            interest_amount = abs(current_balance) * monthly_rate
            
            new_balance = current_balance - interest_amount
            self._set_balance(new_balance)
            
            print(f"📉 Debt Interest Charged: Rs. {interest_amount:.2f}")
            self.log_transaction("Debt Interest Charge", -interest_amount)

    def get_available_credit(self):
        return self.credit_limit + self.get_balance()
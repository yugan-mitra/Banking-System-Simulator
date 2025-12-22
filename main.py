import csv
import os
from accounts import SavingsAccount, CreditAccount

# Folder Paths
DB_ROOT = 'database'
MASTER_FILE = os.path.join(DB_ROOT, 'banking_master.csv')
RECORDS_ROOT = os.path.join(DB_ROOT, 'records')
SAVING_DIR = os.path.join(RECORDS_ROOT, 'saving')
CREDIT_DIR = os.path.join(RECORDS_ROOT, 'credit')

def initialize_system():
    folders = [DB_ROOT, RECORDS_ROOT, SAVING_DIR, CREDIT_DIR]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# --- MASTER DATABASE HANDLING ---

def save_master_data(accounts):
    try:
        with open(MASTER_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'AccNum', 'Name', 'CurrentBalance', 'Rate_Limit', 'MinBal_Fee'])
            
            for acc in accounts:
                if isinstance(acc, SavingsAccount):
                    writer.writerow(['SAVINGS', acc.account_number, acc.holder_name, f"{acc.get_balance():.2f}", acc.interest_rate, acc.min_balance])
                elif isinstance(acc, CreditAccount):
                    writer.writerow(['CREDIT', acc.account_number, acc.holder_name, f"{acc.get_balance():.2f}", acc.credit_limit, 'N/A'])
    except Exception as e:
        print(f"⚠️ Error saving master data: {e}")

def load_master_data():
    accounts = []
    if not os.path.exists(MASTER_FILE):
        return []

    try:
        with open(MASTER_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if not row: continue
                
                acc_type = row[0]
                acc_num = int(row[1])
                name = row[2]
                balance = float(row[3])

                if acc_type == 'SAVINGS':
                    acc = SavingsAccount(name, balance, acc_num, float(row[4]), float(row[5]))
                    accounts.append(acc)
                elif acc_type == 'CREDIT':
                    acc = CreditAccount(name, balance, acc_num, float(row[4]))
                    accounts.append(acc)
                    
    except ValueError:
        print("⚠️ Master file corrupted.")
    
    return accounts

# --- INPUT HELPERS ---

def get_valid_input(prompt, data_type):
    attempts = 0
    while attempts < 3:
        try:
            return data_type(input(prompt))
        except ValueError:
            print("⚠️ Invalid format!")
            attempts += 1
    return None

def find_account(accounts):
    acc_num = get_valid_input("Enter Account Number: ", int)
    if acc_num is None: return None
    for acc in accounts:
        if acc.account_number == acc_num:
            return acc
    print("❌ Account not found.")
    return None

# --- MENU FUNCTIONS ---

def create_account(accounts):
    print("\n--- Open New Account ---")
    
    # 1. choose account type
    print("1. Savings Account (Min Deposit: Rs. 500)")
    print("2. Credit Account  (Min Deposit: Rs. 5000)")
    type_choice = get_valid_input("Select Account Type (1 or 2): ", int)
    
    if type_choice not in [1, 2]:
        print("❌ Invalid choice.")
        return

    name = input("Enter Holder Name: ")
    if not name: return

    # 2. withdrawal amount
    initial_deposit = get_valid_input("Enter Initial Deposit Amount: ", float)
    if initial_deposit is None: return

    # 3. Validation Logic
    new_acc = None
    
    if type_choice == 1: # Savings
        if initial_deposit < 500.00:
            print("❌ Error: Minimum initial deposit for Savings Account is Rs. 500.00")
            return
        new_acc = SavingsAccount(name, initial_deposit)

    elif type_choice == 2: # Credit
        if initial_deposit < 5000.00:
            print("❌ Error: Minimum initial deposit for Credit Account is Rs. 5000.00")
            return
        new_acc = CreditAccount(name, initial_deposit)
    
    accounts.append(new_acc)
    print(f"✅ Account Created Successfully! Number: {new_acc.account_number}")
    save_master_data(accounts)

def perform_transaction(accounts, trans_type):
    acc = find_account(accounts)
    if not acc: return

    print(f"Current Balance: Rs. {acc.get_balance():.2f}")

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        amount = get_valid_input(f"Enter amount to {trans_type}: ", float)

        # If input validator failed (after its own retries), count as a failed attempt
        if amount is None:
            print(f"❌ Invalid input (attempt {attempt}/{max_attempts}).")
            if attempt == max_attempts:
                print("❌ Too many invalid attempts. Returning to main menu.")
                return
            continue

        success = False
        if trans_type == "deposit":
            success = acc.deposit(amount)
        elif trans_type == "withdraw":
            success = acc.withdraw(amount)
        else:
            print("❌ Unknown transaction type.")
            return

        if success:
            save_master_data(accounts)
            return
        else:
            print(f"❌ Transaction failed (attempt {attempt}/{max_attempts}).")
            if attempt == max_attempts:
                print("❌ Maximum attempts reached. Returning to main menu.")
                return
            else:
                print(f"Current Balance: Rs. {acc.get_balance():.2f}")
                # show updated balance and continue to next attempt
                continue

def end_of_month_process(accounts):
    print("\n--- End of Month Processing ---")
    for acc in accounts:
        if isinstance(acc, SavingsAccount):
            acc.apply_interest()
        elif isinstance(acc, CreditAccount):
            acc.apply_debt_interest()
    
    save_master_data(accounts)
    print("✅ All accounts updated and saved.")

def main():
    initialize_system()
    accounts = load_master_data()
    print(f"🔄 System Loaded: {len(accounts)} accounts found.")

    while True:
        print("\n=== 🏦 LKR BANKING SYSTEM ===")
        print("1. Open Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Show All Accounts")
        print("5. Month-End Process")
        print("6. Exit")

        choice = input("Select: ")

        if choice == '1':
            create_account(accounts)
        elif choice == '2':
            perform_transaction(accounts, "deposit")
        elif choice == '3':
            perform_transaction(accounts, "withdraw")
        elif choice == '4':
            print("\n--- Account Registry ---")
            for acc in accounts: print(acc)
        elif choice == '5':
            end_of_month_process(accounts)
        elif choice == '6':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
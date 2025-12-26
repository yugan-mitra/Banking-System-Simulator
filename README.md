# Banking System Simulator

A Python-based banking system simulator for managing bank accounts.

## Features

### Account Types

#### 1. Savings Account (`SavingsAccount`)
- **Account Numbers**: Starts from 1200
- **Features**:
  - Annual Interest Rate: 4%
  - Minimum Balance Requirement: Rs. 500
  - Minimum Withdrawal Amount: Rs. 50
  - Withdrawal Fee: Rs. 5 (for regular withdrawals)
- **Interest Calculation**: Applied monthly to the account balance

#### 2. Credit Account (`CreditAccount`)
- **Account Numbers**: Starts from 1900
- **Features**:
  - Default Credit Limit: Rs. 5,000
  - Debt Interest Rate: 15% (Annual)
  - Cash Advance Fee: 3% (of withdrawal amount)
  - Minimum Cash Advance: Rs. 500
- **Credit Management**: Tracks available credit and debt interest

## Project Structure

```
Banking System Simulator/
│
├── accounts/                      # Account classes package
│   ├── __init__.py               # Package initialization
│   ├── constants.py              # System-wide constants
│   ├── base_account.py           # Abstract base class
│   ├── savings_account.py        # Savings account implementation
│   └── credit_account.py         # Credit account implementation
│
├── database/                      # Data storage
│   ├── banking_master.csv        # Master account database
│   └── records/                  # Transaction logs
│       ├── saving/               # Savings account transactions
│       └── credit/               # Credit account transactions
│
├── database_manager.py           # Database operations (save/load)
├── input_utils.py                # Input validation utilities
├── account_operations.py         # Business logic operations
├── ui.py                         # User interface and menus
├── main.py                       # Application entry point
│
├── accounts.py.backup            # Deprecated (old monolithic file)
├── README.md                     # This file
├── API_DOCUMENTATION.md          # Detailed API reference
└── PROJECT_STRUCTURE.md          # Architecture documentation

```

### File Descriptions

#### `accounts/` Package

##### `constants.py`
Centralized configuration file containing all system-wide constants:
- Database paths (`DB_ROOT`, `MASTER_FILE`, `RECORDS_ROOT`, `SAVING_DIR`, `CREDIT_DIR`)
- Transaction headers
- Date/Time formats
- Currency precision settings
- Application configuration (input attempts, deposit limits)
- Account type identifiers

##### `base_account.py`
Abstract base class for all account types:
- `BankAccount` class with common functionality:
  - Account number generation and management
  - Balance management and tracking
  - Transaction logging to CSV files
  - Deposit and withdrawal operations
  - String representations for debugging

##### `savings_account.py`
Savings account specific implementation:
- `SavingsAccount` class inheriting from `BankAccount`
- Monthly interest calculation
- Minimum balance enforcement
- Withdrawal fee handling
- Special fee-skipping for transfers

##### `credit_account.py`
Credit account specific implementation:
- `CreditAccount` class inheriting from `BankAccount`
- Credit limit management
- Cash advance fee calculation
- Debt interest charging on negative balances
- Available credit tracking

##### `__init__.py`
Package initialization module:
- Exports all public classes and constants
- Version information
- Clean public API for the accounts module

#### Core Application Modules

##### `database_manager.py` (150 lines)
Handles all database operations:
- `save_master_data()`: Saves all accounts to CSV
- `load_master_data()`: Loads accounts from CSV
- `_account_to_row()`: Converts account to CSV row
- `_row_to_account()`: Converts CSV row to account object
- Error handling for file I/O operations

##### `input_utils.py` (50 lines)
Provides input validation and helper functions:
- `get_valid_input()`: Gets validated user input with retry logic
- `find_account()`: Finds an account by number with error handling
- Type conversion and validation

##### `account_operations.py` (230 lines)
Contains all business logic for account operations:
- `create_account()`: Creates new savings or credit accounts
- `perform_transaction()`: Handles deposits and withdrawals
- `transfer_money()`: Transfers funds between accounts with rollback
- `display_all_accounts()`: Lists all registered accounts
- `end_of_month_process()`: Applies interest/debt charges
- `_create_account_by_type()`: Account type validation
- `_execute_transaction()`: Transaction execution
- `_handle_failed_attempt()`: Error message handling

##### `ui.py` (60 lines)
Manages user interface and menu flow:
- `display_menu()`: Shows main menu options
- `handle_menu_choice()`: Routes menu selections to appropriate functions
- Menu-to-function mapping via dictionary

##### `main.py` (35 lines)
Simplified application entry point:
- `initialize_system()`: Creates required database directories
- `main()`: Orchestrates system initialization and main loop
- Imports and coordinates all other modules

#### `accounts.py.backup` [DEPRECATED]
⚠️ **This file is no longer used!** All code has been migrated to the modular structure. Kept for reference only.

## Installation

### Requirements
- Python 3.10+
- No external dependencies (standard library only)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yugan-mitra/Banking-System-Simulator.git
cd "Banking System Simulator"
```

2. Run the application:
```bash
python main.py
```

## Usage

### Running the Application

```bash
python main.py
```

### Main Menu Options

```
=========================================
   🏦 BANKING SYSTEM SIMULATOR 🏦
=========================================
1. Create New Savings Account
2. Create New Credit Account
3. Deposit Money
4. Withdraw Money
5. Check Account Balance
6. View Transaction History
7. Transfer Funds
8. Apply Interest (Savings) / Debt Interest (Credit)
9. List All Accounts
0. Exit
=========================================
```

### Example Usage

#### 1. Creating a Savings Account
```
Select option: 1
Enter holder name: John Doe
Enter initial deposit (minimum Rs. 500.00): 1000

✅ Savings Account Created Successfully!
Account Number: 1200
Initial Balance: Rs. 1000.00
```

#### 2. Creating a Credit Account
```
Select option: 2
Enter holder name: Jane Smith
Enter initial deposit (minimum Rs. 5000.00): 5000

✅ Credit Account Created Successfully!
Account Number: 1900
Initial Balance: Rs. 5000.00
Available Credit: Rs. 10000.00
```

#### 3. Making a Deposit
```
Select option: 3
Enter account number: 1200
Enter deposit amount: Rs. 500

✅ Deposited Rs. 500.00. New Balance: Rs. 1500.00
```

#### 4. Withdrawing Money

**Savings Account:**
```
Select option: 4
Enter account number: 1200
Enter withdrawal amount: Rs. 200

✅ Withdrew Rs. 200.00. New Balance: Rs. 1295.00
💳 Withdrawal fee of Rs. 5.00 applied.
```

**Credit Account:**
```
Select option: 4
Enter account number: 1900
Enter withdrawal amount: Rs. 1000

✅ Withdrew Rs. 1000.00 (Fee: Rs. 30.00). New Balance: Rs. 3970.00
```

#### 5. Transferring Funds
```
Select option: 7
Enter source account number: 1200
Enter destination account number: 1201
Enter transfer amount: Rs. 300

✅ Transfer Successful!
From Account 1200: Rs. 300.00 transferred
To Account 1201: Rs. 300.00 received
```

#### 6. Viewing Transaction History
```
Select option: 6
Enter account number: 1200

📊 Transaction History for Account 1200
========================================
Date       | Time     | Transaction        | Amount    | Balance
-----------|----------|--------------------|-----------|---------
2025-12-26 | 14:30:25 | Account Created    | 1000.00   | 1000.00
2025-12-26 | 14:35:10 | Deposit            | 500.00    | 1500.00
2025-12-26 | 14:40:15 | Withdrawal         | -200.00   | 1300.00
2025-12-26 | 14:40:15 | Withdrawal Fee     | -5.00     | 1295.00
```

## Data Storage

### Master Database (`banking_master.csv`)
Saves the current state of all accounts:
```csv
Type,AccNum,Name,CurrentBalance,Rate_Limit,MinBal_Fee
SAVINGS,1200,John Doe,1295.00,0.04,500.00
CREDIT,1900,Jane Smith,3970.00,5000.00,N/A
```

### Transaction Logs (`database/records/`)
Separate CSV file for each account with transaction history:
```csv
Date,Time,Transaction,Amount,New Balance
2025-12-26,14:30:25,Account Created,1000.00,1000.00
2025-12-26,14:35:10,Deposit,500.00,1500.00
2025-12-26,14:40:15,Withdrawal,-200.00,1300.00
2025-12-26,14:40:15,Withdrawal Fee,-5.00,1295.00
```

## Technical Details

### Object-Oriented Design

#### Class Hierarchy
```
BankAccount (ABC)
├── SavingsAccount
└── CreditAccount
```

#### Key Design Patterns
1. **Abstract Base Class**: `BankAccount` provides a common interface
2. **Inheritance**: Account types inherit and extend base functionality
3. **Encapsulation**: Balance and internal state are protected (`_balance`)
4. **Type Hints**: Modern Python type hints are used throughout
5. **ClassVar**: Uses class-level counters for account numbering

### Account Number Management

#### Savings Accounts
- Base number: 1200
- Sequential: 1200, 1201, 1202, ...
- Managed by: `SavingsAccount._next_account_number`

#### Credit Accounts
- Base number: 1900
- Sequential: 1900, 1901, 1902, ...
- Managed by: `CreditAccount._next_account_number`

### Transaction Logging

Each transaction is logged to CSV files with a timestamp:
- Date: `YYYY-MM-DD` format
- Time: `HH:MM:SS` format
- Transaction type description
- Amount (positive for credits, negative for debits)
- Running balance

### Error Handling

The application has comprehensive validation and error handling:
- Input validation (amounts, account numbers)
- Balance checks (insufficient funds, minimum balance)
- File I/O error handling
- Type conversion error handling

## API Reference

### `BankAccount` (Abstract Base Class)

#### Methods
- `__init__(holder_name, initial_balance, account_number, record_folder)`
- `deposit(amount) -> bool`: Deposits money into the account
- `withdraw(amount) -> bool`: Withdraws money from the account
- `get_balance() -> float`: Returns the current balance
- `_log_transaction(transaction_type, amount)`: Logs a transaction

#### Properties
- `balance`: Current balance (read-only)
- `account_number`: Account number
- `holder_name`: Account holder name

### `SavingsAccount`

#### Additional Methods
- `apply_interest()`: Applies monthly interest

#### Constants
- `MIN_WITHDRAWAL_AMOUNT = 50.00`
- `WITHDRAWAL_FEE = 5.00`
- `DEFAULT_INTEREST_RATE = 0.04`
- `DEFAULT_MIN_BALANCE = 500.00`

### `CreditAccount`

#### Additional Methods
- `apply_debt_interest()`: Charges debt interest
- `get_available_credit() -> float`: Returns available credit

#### Properties
- `available_credit`: Remaining credit amount (read-only)

#### Constants
- `MIN_CASH_ADVANCE_AMOUNT = 500.00`
- `DEFAULT_CREDIT_LIMIT = 5000.00`
- `DEFAULT_DEBT_INTEREST_RATE = 0.15`
- `DEFAULT_CASH_ADVANCE_FEE = 0.03`

## Development

### Code Organization

The project follows a modular architecture with clear separation of concerns:

- **accounts/** - Domain models (account classes)
- **database_manager.py** - Data access layer
- **input_utils.py** - Input validation
- **account_operations.py** - Business logic
- **ui.py** - User interface
- **main.py** - Application entry point

This structure makes the code:
- Easy to understand and navigate
- Simple to test and extend
- Maintainable and scalable

### Code Style
- PEP 8 compliant
- Type hints used throughout
- Comprehensive docstrings
- Descriptive variable names
- Modular and testable design

### Testing Recommendations
1. Unit tests for account operations
2. Integration tests for database operations
3. Input validation tests
4. Transfer functionality tests
5. Edge cases (negative amounts, exceeding limits)
6. File I/O tests

## License

Created for educational purposes.

## Contributing

Contributions for improvements and bug fixes are welcome!

## Contact

If you have any questions, please contact the project maintainer.

---

**Version**: 1.0.0  
**Last Updated**: December 26, 2025

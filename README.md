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
├── accounts/                      # Accounts package
│   ├── __init__.py               # Package initialization
│   ├── constants.py              # System constants
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
├── main.py                       # Main application
├── accounts.py                   # [DEPRECATED - See details below]
└── README.md                     # This file

```

### File Descriptions

#### `accounts/` Package

##### `constants.py`
File defining all system-wide constants:
- Database paths (`DB_ROOT`, `RECORDS_ROOT`)
- Transaction headers
- Date/Time formats
- Currency precision settings

##### `base_account.py`
Abstract base class for all account types:
- `BankAccount` class: All common functionality
  - Account number generation
  - Balance management
  - Transaction logging
  - Deposit/Withdrawal operations

##### `savings_account.py`
Savings account implementation:
- `SavingsAccount` class
- Monthly interest calculation
- Minimum balance enforcement
- Withdrawal fees and restrictions

##### `credit_account.py`
Credit account implementation:
- `CreditAccount` class
- Credit limit management
- Cash advance fees
- Debt interest calculation

##### `__init__.py`
Package initialization and clean imports:
- Exposes all classes
- Version information
- Package-level exports

#### `main.py`
Main application file:
- Menu-driven user interface
- Account management operations:
  - Create new accounts
  - Deposit/Withdraw
  - Check balance
  - View transaction history
  - Transfer funds
- Master database operations (save/load)
- Input validation and error handling

#### `accounts.py` [DEPRECATED]
⚠️ **This file is no longer used!** All code has been moved to the `accounts/` package. It is kept to maintain backward compatibility. Use the `accounts/` package for new code.

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

### Code Style
- PEP 8 compliant
- Type hints used throughout
- Comprehensive docstrings
- Descriptive variable names

### Testing Recommendations
1. Account creation tests
2. Deposit/Withdrawal validation tests
3. Interest calculation tests
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

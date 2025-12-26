from pathlib import Path
from typing import Final

# =============================================================================
# Database Configuration
# =============================================================================
DB_ROOT: Final[str] = "database"
MASTER_FILE: Final[Path] = Path(DB_ROOT) / "banking_master.csv"
RECORDS_ROOT: Final[Path] = Path(DB_ROOT) / "records"
SAVING_DIR: Final[Path] = RECORDS_ROOT / "saving"
CREDIT_DIR: Final[Path] = RECORDS_ROOT / "credit"

# =============================================================================
# Transaction Log Configuration
# =============================================================================
TRANSACTION_HEADERS: Final[tuple[str, ...]] = (
    "Date", "Time", "Transaction", "Amount", "New Balance"
)

# =============================================================================
# Date/Time Formats
# =============================================================================
DATE_FORMAT: Final[str] = "%Y-%m-%d"
TIME_FORMAT: Final[str] = "%H:%M:%S"

# =============================================================================
# Currency Configuration
# =============================================================================
CURRENCY_PRECISION: Final[int] = 2

# =============================================================================
# Application Configuration
# =============================================================================
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

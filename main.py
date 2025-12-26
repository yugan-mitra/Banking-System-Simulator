"""
Banking System Simulator

Main entry point for the application.
Orchestrates system initialization and the main application loop.
"""

from pathlib import Path

from accounts import DB_ROOT, RECORDS_ROOT, SAVING_DIR, CREDIT_DIR
from database_manager import load_master_data
from ui import display_menu, handle_menu_choice


def initialize_system() -> None:
    """Create required database directories if they don't exist."""
    directories = [DB_ROOT, RECORDS_ROOT, SAVING_DIR, CREDIT_DIR]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Main entry point for the banking system simulator."""
    initialize_system()
    accounts = load_master_data()
    
    print(f"🔄 System Loaded: {len(accounts)} accounts found.")

    running = True
    while running:
        display_menu()
        choice = input("Select: ").strip()
        running = handle_menu_choice(choice, accounts)


if __name__ == "__main__":
    main()
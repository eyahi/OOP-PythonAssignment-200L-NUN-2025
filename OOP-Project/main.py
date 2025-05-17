# main.py
"""
Main entry point for the Password Manager application.
"""

import getpass
import os
import sys
import time
from password_manager import PasswordManager

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    clear_screen()
    print("=" * 50)
    print("             SECURE PASSWORD MANAGER             ")
    print("=" * 50)
    print()

def get_master_password(for_verification=False):
    """
    Prompt the user for the master password.
    
    Args:
        for_verification (bool): Whether to prompt for verification
        
    Returns:
        str: The entered master password
    """
    if for_verification:
        return getpass.getpass("Enter your master password: ")
    
    while True:
        password = getpass.getpass("Create a master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        
        if password == confirm:
            return password
        
        print("Passwords do not match. Please try again.")

def initialize_password_manager():
    """
    Initialize or load the password manager.
    
    Returns:
        PasswordManager: The initialized password manager
    """
    data_file = "passwords.json"
    
    if os.path.exists(data_file):
        # File exists, load existing data
        while True:
            master_password = get_master_password(for_verification=True)
            password_manager = PasswordManager(master_password, data_file)
            
            if password_manager.verify_master_password(master_password):
                print("Password manager unlocked successfully!")
                time.sleep(1)
                return password_manager
            else:
                print("Incorrect master password. Please try again.")
                time.sleep(1)
    else:
        # Create new password manager
        print("No existing password file found. Creating a new one.")
        master_password = get_master_password()
        password_manager = PasswordManager(master_password, data_file)
        print("Password manager created successfully!")
        time.sleep(1)
        return password_manager

def display_menu():
    """Display the main menu."""
    print("\nMenu:")
    print("1. Add a new password")
    print("2. Retrieve a password")
    print("3. Update a password")
    print("4. Delete a password")
    print("5. List all websites/services")
    print("6. Save and exit")
    print("7. Exit without saving")
    
    choice = input("\nEnter your choice (1-7): ")
    return choice

def add_password(password_manager):
    """Add a new password entry."""
    print_header()
    print("ADD NEW PASSWORD\n")
    
    website = input("Enter website/service name: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    if password_manager.add_password(website, username, password):
        print(f"\nPassword for {website} added successfully!")
    else:
        print(f"\nEntry for {website} already exists. Use the update option.")
    
    input("\nPress Enter to continue...")

def retrieve_password(password_manager):
    """Retrieve a password entry."""
    print_header()
    print("RETRIEVE PASSWORD\n")
    
    website = input("Enter website/service name: ")
    username, password = password_manager.get_password(website)
    
    if username and password:
        print(f"\nWebsite: {website}")
        print(f"Username: {username}")
        print(f"Password: {password}")
    else:
        print(f"\nNo entry found for {website}.")
    
    input("\nPress Enter to continue...")

def update_password(password_manager):
    """Update an existing password entry."""
    print_header()
    print("UPDATE PASSWORD\n")
    
    website = input("Enter website/service name: ")
    
    # Check if the entry exists
    username, _ = password_manager.get_password(website)
    if not username:
        print(f"\nNo entry found for {website}.")
        input("\nPress Enter to continue...")
        return
    
    print(f"\nCurrent username for {website}: {username}")
    
    new_username = input("Enter new username (leave blank to keep current): ")
    if not new_username:
        new_username = username
    
    new_password = getpass.getpass("Enter new password (leave blank to keep current): ")
    if not new_password:
        _, new_password = password_manager.get_password(website)
    
    if password_manager.update_password(website, new_username, new_password):
        print(f"\nPassword for {website} updated successfully!")
    else:
        print(f"\nFailed to update password for {website}.")
    
    input("\nPress Enter to continue...")

def delete_password(password_manager):
    """Delete a password entry."""
    print_header()
    print("DELETE PASSWORD\n")
    
    website = input("Enter website/service name: ")
    
    # Check if the entry exists
    username, _ = password_manager.get_password(website)
    if not username:
        print(f"\nNo entry found for {website}.")
        input("\nPress Enter to continue...")
        return
    
    confirm = input(f"Are you sure you want to delete the entry for {website}? (y/n): ")
    if confirm.lower() == 'y':
        if password_manager.delete_password(website):
            print(f"\nEntry for {website} deleted successfully!")
        else:
            print(f"\nFailed to delete entry for {website}.")
    else:
        print("\nDeletion cancelled.")
    
    input("\nPress Enter to continue...")

def list_websites(password_manager):
    """List all stored websites/services."""
    print_header()
    print("STORED WEBSITES/SERVICES\n")
    
    websites = password_manager.list_websites()
    
    if websites:
        for i, website in enumerate(sorted(websites), 1):
            print(f"{i}. {website}")
    else:
        print("No passwords stored yet.")
    
    input("\nPress Enter to continue...")

def main():
    """Main function of the password manager application."""
    try:
        password_manager = initialize_password_manager()
        
        while True:
            print_header()
            choice = display_menu()
            
            if choice == '1':
                add_password(password_manager)
            elif choice == '2':
                retrieve_password(password_manager)
            elif choice == '3':
                update_password(password_manager)
            elif choice == '4':
                delete_password(password_manager)
            elif choice == '5':
                list_websites(password_manager)
            elif choice == '6':
                password_manager.save_to_file()
                print("\nChanges saved successfully!")
                print("Exiting Password Manager...")
                time.sleep(1)
                break
            elif choice == '7':
                confirm = input("\nExit without saving changes? (y/n): ")
                if confirm.lower() == 'y':
                    print("Exiting Password Manager without saving...")
                    time.sleep(1)
                    break
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
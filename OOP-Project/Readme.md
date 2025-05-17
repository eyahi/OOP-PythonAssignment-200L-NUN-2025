# Secure Password Manager

Provided By : Ibrahim DIkko (201203058) & Almustapha Ahmed (201203033)
      
A simple command-line password manager built with Python that allows you to securely store, retrieve, and manage your passwords.

## Features

- **Secure Storage**: All passwords are encrypted before storage
- **Master Password Protection**: Access to stored passwords requires authentication
- **Easy Management**: Simple interface to add, retrieve, update, and delete passwords
- **Data Persistence**: Password data is saved to a file for persistence between sessions

## Project Structure

```
password-manager/
│
├── main.py                # Main application entry point
├── password_manager.py    # Password Manager class
├── password_entry.py      # Password Entry class
├── encryption_util.py     # Encryption utilities
└── passwords.json         # Encrypted password data (created on first run)
```

## Requirements

- Python 3.11
- cryptography package

1. Install the required dependencies:
```
pip install cryptography
```

## Usage

1. Run the application:
```
python main.py
```

2. First-time setup:
   - Create a master password when prompted
   - Remember this password as it cannot be recovered

3. Managing Passwords:
   - Use the menu options to add, retrieve, update, or delete password entries
   - All data is automatically saved when you exit using the "Save and exit" option

## Security Notes

- **Master Password**: Choose a strong master password that you can remember
- **Data File**: The `passwords.json` file contains your encrypted passwords. Keep it safe.
- **No Recovery**: If you forget your master password, there is no way to recover your stored passwords

## Future Enhancements

- Password strength checker
- Auto-generated secure passwords
- Clipboard integration
- Backup and restore functionality
- GUI interface

# Password Manager

OOP (Python) semester project

This is a secure offline desktop password manager built in Python, demonstrating Object-Oriented Programming (OOP) concepts and encryption. The application supports both a Command-Line Interface (CLI) and a Graphical User Interface (GUI) built with Tkinter.

---

## Features

- **Secure password storage:** Passwords are stored in an encrypted file using a custom encryption utility.
- **OOP architecture:** Classes for password entries, management, and encryption utilities.
- **CLI & GUI:** Use either the command line or a Tkinter-based desktop interface.
- **Password generation:** Built-in random password generator (GUI).
- **Master password protection:** Access is restricted by a master password.
- **CRUD operations:** Add, retrieve, update, and delete password entries.
- **Search & autofill (GUI):** Quickly find and autofill saved credentials.

---

## Project Structure

```
password-manager/
├── main.py                # Entry point for CLI and GUI
├── password_manager.py    # Password management logic (add, update, delete, save/load)
├── password_entry.py      # Password entry class (website, username, password)
├── encryption_util.py     # Encryption/Decryption of stored data
├── ui.py                  # Tkinter-based GUI
├── passwords.json         # (Created at runtime) Encrypted password storage
├── README.md              # Project documentation
└── logo.png               # (Optional) Logo for the GUI
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Tkinter (usually included with Python)
- No external dependencies required

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/zlea-x/password-manager.git
    cd password-manager
    ```

2. **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

---

## Usage

### 1. **Graphical User Interface (GUI)**

Just run:
```bash
python ui.py
```
- Enter the master password when prompted.
- Add, search, generate, and delete password entries using the buttons and forms.
- Passwords are saved encrypted locally in `passwords.json`.

### 2. **Command-Line Interface (CLI)**

Run:
```bash
python password_manager.py
```
- Enter the master password at the prompt.
- Use the menu to add, retrieve, update, or delete password entries.

### 3. **Testing & Demos**

- `main.py` contains example/test routines for:
    - Password entry creation and serialization
    - Encryption/Decryption testing
    - PasswordManager CRUD operations

---

## Security Notes

- All passwords are saved in an encrypted form.
- Access to the manager is protected by a hardcoded master password (`OOP-project` by default). **For real-world use, update this for security!**
- The encryption utility is custom; for production, use proven libraries (e.g., `cryptography`).

---

## Example

**CLI Example:**
```
Enter Master Password: OOP-project

Password Manager CLI
1. Add password
2. Retrieve password
3. Update password
4. Delete password
5. Exit
Enter choice:
```

**GUI Example:**

- Click "Add Password" to store a new entry.
- Use "Generate" to create a strong random password.
- Use "Search" to autofill credentials for a website.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or pull request.

---

## License

This project is for educational purposes. For any use beyond coursework, please contact the author or check with your instructor.

---

## Acknowledgments

Developed as a semester project for OOP (Python).

---

## Authors
-[Anuri Joy Philemon](https://github.com/joycrates)
-[Azalea Akpokugbe](https://github.com/zlea-x)

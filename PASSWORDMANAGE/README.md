
# 🔐 Password Manager

A secure desktop application to store and manage website credentials. It provides an intuitive UI, encrypted password storage, and basic CRUD functionality using SQLite and Python.

---

## 📌 Features

### ✅ Core Functionality
- **Master Password Login**: Access is protected with a configurable master password.
- **Add Records**: Securely add website credentials (website, username, password).
- **View Records**: Display all saved records in a sortable Treeview.
- **Update/Delete Records**: Modify or remove existing entries.
- **Copy Password**: Quickly copy passwords to clipboard with one click.
- **Encrypted Passwords**: Passwords are stored securely using `cryptography.Fernet`.
- **Masked Input**: Password entry fields are hidden by default.
- **Popup Notifications**: Temporary feedback for successful operations or errors.

---

## 📁 Project Structure

```plaintext
├── password manager.py      # Main GUI application
├── db_operations.py         # Handles database and encryption logic
├── secret.key               # Auto-generated key for encrypting passwords
├── password_records.db      # Local SQLite database (auto-created)
```

---

## 🔒 Security & Encryption

- Uses `cryptography.Fernet` for symmetric encryption (AES).
- A unique encryption key is generated and stored in `secret.key`.
- Only the password field is encrypted in the database.
- `secret.key` is critical; if lost, encrypted passwords become unrecoverable.

---

## 🛠 Setup Instructions

### 📦 Requirements
- Python 3.7 or higher
- Required Python packages:
  ```bash
  pip install cryptography
  ```

### ▶ How to Run
```bash
python "password manager.py"
```

---

## 🔐 Master Password

The master password is **hardcoded** in the application for demonstration purposes.

- The default master password is:
  ```
  admin123
  ```
- **To change** the master password, edit the following line in `password manager.py`:
  ```python
  if entered_password == "admin123":
  ```

---

## 🚧 Planned Enhancements

- [ ] Implement search functionality for website/username
- [ ] Add master password change feature
- [ ] Include password strength meter
- [ ] Integrate a password generator
- [ ] Export/import database with encryption
- [ ] Toggle password visibility in entry field

---

## 🧪 Testing

You can test the current features by:
1. Running the application
2. Logging in using the master password (`admin123`)
3. Adding new records and verifying encryption by checking the `password_records.db`
4. Testing copy password and update/delete functionality

---

## 🧠 Usage Tips

- To reset encryption (for testing), delete the `secret.key` and `password_records.db` files.  
  ⚠ **This will erase all stored data!**

- Keep `secret.key` safe and never share it. Losing this file means losing access to all encrypted passwords.

---

## 👨‍💻 Authors

Developed with Python by a security-conscious developer using:
- `tkinter` for GUI
- `sqlite3` for local storage
- `cryptography` for encryption

---

## ⚠ Disclaimer

This tool is intended for educational and personal use. For handling sensitive credentials, professional-grade tools (like Bitwarden or 1Password) are recommended.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

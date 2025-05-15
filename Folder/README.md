# Password Manager (Python GUI with OOP)

This is a simple yet secure **Password Manager** built using **Python**, **Tkinter**, and **Object-Oriented Programming (OOP)** principles. It provides a GUI for users to store, retrieve, update, and delete passwords, all secured with **encryption** and protected by a **master password**.

## Features

- Master password authentication
- Add, search, update, and delete password entries
- Passwords stored in encrypted format using cryptography
- GUI built with Tkinter to resemble a clean and simple layout
- Data stored securely in a local .json file
- Uses encapsulation via private attributes and getters/setters



## Getting Started

### 1. Install Dependencies

Make sure you have Python 3 installed. Then install the required packages:

```bash
pip install cryptography
pip install  pyperclip
```

### 2. **Run the Application**

```bash
python password_manager_gui.py
```

### 3. First-Time Use

- You'll be prompted for a master password (used for encrypting/decrypting your saved data).
- Make sure to **remember your master password**. You cannot recover data without it.

---


---

## Oriented Concepts Used

- **Encapsulation**: `PasswordEntry` uses private attributes with getter/setter methods.
- **File I/O**: Passwords are encrypted and saved/loaded from a JSON file.

---


## License

This project is made by Abdulrahman Mohammed, Suleiman Baba Ahmed and Safiya Abubakar for educational purposes, You are free to coopy and spread it however you wish.
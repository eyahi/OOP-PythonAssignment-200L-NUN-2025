---

My Diary - Python OOP Diary Application

Overview: My Diary is a pink-themed GUI-based diary application developed in Python. It is designed as a simple, elegant, and minimal app that allows users to write, save, edit, search, and delete diary entries. This project is built entirely with Object-Oriented Programming (OOP) concepts and uses the tkinter library for the graphical interface.


---

Features:

Create New Entry: Start a fresh diary entry with a title and content.

Save Entry: Save the current entry. It is stored as a .txt file using the title as the filename.

View Saved Entries: Displays a list of all previously saved entries on the left panel.

Delete Entry: Deletes the currently selected diary entry.

Search Entry: Search for specific entries by title keyword.

Auto Date-Time Display: Displays the current date and time at the bottom left. Updates when a new entry is saved or modified.

Responsive Layout: The interface adjusts smoothly to full screen or resized windows.



---

How to Run the App:

1. Ensure you have Python 3 installed on your system.


2. Open the project in PyCharm or any Python IDE.


3. Run the main.py file.


4. The graphical interface will launch, and you can start using the diary.




---

Project Structure:

main.py — Entry point of the program. It initializes and launches the app.

gui.py — Contains all the graphical user interface logic using tkinter.

diary.py — Manages the DiaryEntry class and handles saving, loading, deleting diary entries.



---

Storage Method: All diary entries are stored as .txt files instead of .json. This is because:

It is simpler to implement for text-based notes.

Plain .txt files allow direct readability and editing without needing to parse structured data.


---
AUTHORS
20230025  AMOS AGOR
20231862  BRIGHT FOMAH
20231728  BAQIR MUHAMMAD ALI


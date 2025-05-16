#import 
import json
import os
from password_entry import PasswordEntry
from encryption_util import EncryptionUtil

class PasswordManager:
    def __init__(self, filename="passwords.json"): # initializes passwordmanager and saves data here
        self.filename = filename
        self.passwords = []  # list that'll store the password entries
        self.load_from_file() # loads any existing saved passwords from the file

    def add_password(self, entry: PasswordEntry):
        """
        Adds a new password entry objest to the manager.
        """
        self.passwords.append(entry)  # adds the entry to the list
        self.save_to_file() # saves the updated list to the file

    def get_password(self, website):
        """
        gets a password for an inputed website
        """
        for entry in self.passwords:
            if entry.website == website:
                return entry #returs the password if the website matches
        return None
    
    def update_password(self, website, username, password):
        for entry in self.passwords:
            if entry.website == website:
                entry.username = username
                entry.password = password
                self.save_to_file()
                return True
        return False
    
    def delete_password(self, website):
        self.passwords = [entry for entry in self.passwords if entry.website != website]
        self.save_to_file()

    def save_to_file(self):
        """
        Convert the list of password entries to JSON, encrypt it, and saves it to a file.
        """
        data = [entry.to_dict() for entry in self.passwords]  # Convert each object to a dictionary
        json_data = json.dumps(data)                   # Convert the list of dictionaries to a JSON string
        encrypted = EncryptionUtil.encrypt(json_data)  # Encrypt the JSON string using encryption utility

        with open(self.filename, 'wb') as key_file:           # (wb) Open file in binary write mode
            key_file.write(encrypted)                         # Writes the encrypted data to file

    def load_from_file(self):
        """
        Load and decrypt data from file (if it exists).
        Converts decrypted JSON back into PasswordEntry objects.
        """
        if not os.path.exists(self.filename):
            return                                     # checks and exit if file doesn't exist

        with open(self.filename, 'rb') as key_file:           # (rb) Open file in binary read mode
            encrypted = key_file.read()                       # Read the encrypted data
            try:
                decrypted = EncryptionUtil.decrypt(encrypted)     # trying to decrypt the data using the utility class
                data = json.loads(decrypted)                     # Load JSON string into Python list if the decryption is successful
                # Convert each dictionary back into a PasswordEntry object
                self.passwords = [PasswordEntry.from_dict(entry) for entry in data]
            except Exception as e:
                # Handle decryption or JSON errors
                print(f"Error loading data: {e}")
                self.passwords = []                    # If there's an error, use an empty list

def main():
        manager = PasswordManager()
        MASTER_PASSWORD = "OOP-project"
        entered = input("Enter Master Password: ")
        if entered != MASTER_PASSWORD:
            print("Access Denied.")
            return

        while True:
            print("\nPassword Manager CLI")
            print("1. Add password")
            print("2. Retrieve password")
            print("3. Update password")
            print("4. Delete password")
            print("5. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                site = input("Website: ")
                user = input("Username/Email: ")
                pw = input("Password: ")
                manager.add_password(PasswordEntry(site, user, pw))
                print("Entry added.")
            elif choice == "2":
                site = input("Website: ")
                entry = manager.get_password(site)
                if entry:
                    print(f"Username: {entry.username}\nPassword: {entry.password}")
                else:
                    print("Not found.")
            elif choice == "3":
                site = input("Website to update: ")
                user = input("New Username: ")
                pw = input("New Password: ")
                updated = manager.update_password(site, user, pw)
                print("Updated." if updated else "Not found.")
            elif choice == "4":
                site = input("Website to delete: ")
                manager.delete_password(site)
                print("Entry deleted.")
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()

# This is a simple command-line interface for the PasswordManager class.
# It allows users to add, retrieve, update, and delete password entries.
# The main function initializes the PasswordManager and provides a menu for user interaction.

# A view all option could be added but it won't be because that defeats the purpose of the password manager.
# password_manager.py

import json
import os
from password_entry import PasswordEntry
from encryption_util import encrypt_string, decrypt_string, load_key

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.entries = {}
        self.key = load_key()
        self.load_from_file()

    def add_password(self, website, username, password):
        encrypted_password = encrypt_string(self.key, password)
        entry = PasswordEntry(website, username, encrypted_password)
        self.entries[website] = entry

    def get_password(self, website):
        entry = self.entries.get(website)
        if entry:
            decrypted_password = decrypt_string(self.key, entry.get_password())
            return entry.get_username(), decrypted_password
        return None

    def update_password(self, website, username, password):
        if website in self.entries:
            encrypted_password = encrypt_string(self.key, password)
            self.entries[website].set_username(username)
            self.entries[website].set_password(encrypted_password)

    def delete_password(self, website):
        if website in self.entries:
            del self.entries[website]

    def save_to_file(self):
        data = {
            website: {
                "username": entry.get_username(),
                "password": entry.get_password()
            }
            for website, entry in self.entries.items()
        }
        with open("passwords.json", "w") as file:
            json.dump(data, file)

    def load_from_file(self):
        if os.path.exists("passwords.json"):
            with open("passwords.json", "r") as file:
                data = json.load(file)
                for website, info in data.items():
                    self.entries[website] = PasswordEntry(
                        website, info["username"], info["password"]
                    )

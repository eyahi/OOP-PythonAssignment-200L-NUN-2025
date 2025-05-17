# password_manager.py
"""
Main application file for the Password Manager.
"""

import json
import os
import getpass
import base64
from encryption_util import EncryptionUtil
from password_entry import PasswordEntry

class PasswordManager:
    """
    A class to manage password entries.
    
    Attributes:
        entries (dict): Dictionary of password entries with website as the key
        master_password (str): The master password for the password manager
        key (bytes): The encryption key derived from the master password
        salt (bytes): The salt used for key derivation
        data_file (str): Path to the data file
    """
    
    def __init__(self, master_password, data_file="passwords.json"):
        """
        Initialize a new PasswordManager object.
        
        Args:
            master_password (str): The master password
            data_file (str): Path to the data file
        """
        self.entries = {}
        self.master_password = master_password
        self.data_file = data_file
        self.salt = None
        
        # If data file exists, load from it
        if os.path.exists(data_file):
            self.load_from_file()
        else:
            # Generate a new key and salt
            self.key, self.salt = EncryptionUtil.generate_key(master_password)
    
    def add_password(self, website, username, password):
        """
        Add a new password entry.
        
        Args:
            website (str): The website or service name
            username (str): The username for the service
            password (str): The password for the service
            
        Returns:
            bool: True if successful, False if entry already exists
        """
        if website in self.entries:
            return False
        
        # Encrypt the password
        encrypted_password = EncryptionUtil.encrypt(password, self.key)
        # Store the encrypted password as a base64 string for JSON serialization
        encrypted_password_str = base64.b64encode(encrypted_password).decode('utf-8')
        
        entry = PasswordEntry(website, username, encrypted_password_str)
        self.entries[website] = entry
        return True
    
    def get_password(self, website):
        """
        Retrieve a password entry by website.
        
        Args:
            website (str): The website or service name
            
        Returns:
            tuple: (username, decrypted_password) or (None, None) if not found
        """
        entry = self.entries.get(website)
        if entry is None:
            return None, None
        
        # Decrypt the password
        encrypted_password_bytes = base64.b64decode(entry.get_password())
        decrypted_password = EncryptionUtil.decrypt(encrypted_password_bytes, self.key)
        
        return entry.get_username(), decrypted_password
    
    def update_password(self, website, username, password):
        """
        Update an existing password entry.
        
        Args:
            website (str): The website or service name
            username (str): The username for the service
            password (str): The password for the service
            
        Returns:
            bool: True if successful, False if entry does not exist
        """
        if website not in self.entries:
            return False
        
        # Encrypt the password
        encrypted_password = EncryptionUtil.encrypt(password, self.key)
        # Store the encrypted password as a base64 string for JSON serialization
        encrypted_password_str = base64.b64encode(encrypted_password).decode('utf-8')
        
        entry = self.entries[website]
        entry.set_username(username)
        entry.set_password(encrypted_password_str)
        return True
    
    def delete_password(self, website):
        """
        Delete a password entry.
        
        Args:
            website (str): The website or service name
            
        Returns:
            bool: True if successful, False if entry does not exist
        """
        if website not in self.entries:
            return False
        
        del self.entries[website]
        return True
    
    def list_websites(self):
        """
        List all stored websites/services.
        
        Returns:
            list: List of website names
        """
        return list(self.entries.keys())
    
    def save_to_file(self):
        """
        Save password entries to a file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = {
                "salt": base64.b64encode(self.salt).decode('utf-8'),
                "entries": {
                    website: entry.to_dict() 
                    for website, entry in self.entries.items()
                }
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
            
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False
    
    def load_from_file(self):
        """
        Load password entries from a file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Get the salt and regenerate the key
            self.salt = base64.b64decode(data.get("salt"))
            self.key, _ = EncryptionUtil.generate_key(self.master_password, self.salt)
            
            # Load entries
            entries_data = data.get("entries", {})
            for website, entry_data in entries_data.items():
                entry = PasswordEntry.from_dict(entry_data)
                self.entries[website] = entry
            
            return True
        except Exception as e:
            print(f"Error loading from file: {e}")
            return False
    
    def verify_master_password(self, password):
        """
        Verify if the given password matches the master password.
        
        This is done by trying to decrypt a test entry.
        
        Args:
            password (str): The password to verify
            
        Returns:
            bool: True if verification succeeds, False otherwise
        """
        try:
            test_key, _ = EncryptionUtil.generate_key(password, self.salt)
            
            # Try to decrypt one entry to verify the password
            if self.entries:
                website = next(iter(self.entries))
                entry = self.entries[website]
                encrypted_password_bytes = base64.b64decode(entry.get_password())
                EncryptionUtil.decrypt(encrypted_password_bytes, test_key)
                return True
            
            # If there are no entries, just compare the keys
            return test_key == self.key
        except Exception:
            return False
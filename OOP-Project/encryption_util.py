# encryption_util.py
"""
Utilities for encrypting and decrypting passwords.
"""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionUtil:
    """
    A utility class for encrypting and decrypting strings.
    """
    
    @staticmethod
    def generate_key(master_password, salt=None):
        """
        Generate an encryption key from the master password.
        
        Args:
            master_password (str): The master password
            salt (bytes, optional): Salt for key derivation
            
        Returns:
            tuple: (key, salt) where key is the encryption key and salt is the salt used
        """
        if salt is None:
            salt = os.urandom(16)
        
        # Convert password to bytes if it's a string
        if isinstance(master_password, str):
            master_password = master_password.encode()
        
        # Use PBKDF2 to derive a key from the password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_password))
        return key, salt
    
    @staticmethod
    def encrypt(data, key):
        """
        Encrypt data using the provided key.
        
        Args:
            data (str): The data to encrypt
            key (bytes): The encryption key
            
        Returns:
            bytes: The encrypted data
        """
        if isinstance(data, str):
            data = data.encode()
        
        f = Fernet(key)
        return f.encrypt(data)
    
    @staticmethod
    def decrypt(encrypted_data, key):
        """
        Decrypt data using the provided key.
        
        Args:
            encrypted_data (bytes): The encrypted data
            key (bytes): The encryption key
            
        Returns:
            str: The decrypted data
        """
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
# installed cryptography library for encryption/decryption
from cryptography.fernet import Fernet
import os

class EncryptionUtil:
    KEY_FILE = "secret.key"

    @staticmethod
    def generate_key():
        """
        Generate a key for encryption and save it to a file.
        This key should be kept secret and secure.
        """
        key = Fernet.generate_key()
        with open(EncryptionUtil.KEY_FILE, "wb") as key_file:
            key_file.write(key)

    @staticmethod
    def load_key():
        """
        Load the previously generated key from a file.
        and if the key doesn't exist generate a key
        """
        if not os.path.exists(EncryptionUtil.KEY_FILE):
            EncryptionUtil.generate_key()
        with open(EncryptionUtil.KEY_FILE, "rb") as key_file:
            return key_file.read()
        
    @staticmethod
    def encrypt(data: str) -> bytes:
        """
        encrypt a string and return the encrypted bytes
        """
        key = EncryptionUtil.load_key()
        return Fernet(key).encrypt(data.encode())
    
    @staticmethod
    def decrypt(token: bytes) -> str:
        """
        decrypt the encrypted bytes and return the original string
        """
        key = EncryptionUtil.load_key()
        return Fernet(key).decrypt(token).decode()
    
    
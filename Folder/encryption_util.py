# encryption_util.py

from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_string(key, string):
    f = Fernet(key)
    return f.encrypt(string.encode()).decode()

def decrypt_string(key, encrypted_string):
    f = Fernet(key)
    return f.decrypt(encrypted_string.encode()).decode()



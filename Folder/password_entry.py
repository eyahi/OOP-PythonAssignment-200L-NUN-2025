# password_entry.py

class PasswordEntry:
    def __init__(self, website, username, password):
        self.website = website
        self.__username = username
        self.__password = password

    def get_website(self):
        return self.website

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

class PasswordEntry:
    def __init__(self, website, username, password): #initialize the PasswordEntry object with website, username, and password
        self.website = website
        self.username = username
        self.password = password

    def to_dict(self):
        """
        Convert the PasswordEntry object to a dictionary.
        This is useful for serialization to JSON.
        """
        return {
            "website": self.website,
            "username": self.username,
            "password": self.password
        }

    @staticmethod
    def from_dict(data):
        """
        Create a PasswordEntry object from a dictionary.
        This is useful for deserialization from JSON.
        """
        return PasswordEntry(
            data["website"],
            data["username"],
            data["password"]
        )
        

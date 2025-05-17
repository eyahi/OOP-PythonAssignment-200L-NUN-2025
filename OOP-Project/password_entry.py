# password_entry.py
"""
Class to represent a single password entry in the password manager.
"""

class PasswordEntry:
    """
    A class to represent a single password entry.
    
    Attributes:
        website (str): The website or service name
        username (str): The username for the service
        password (str): The encrypted password for the service
    """
    
    def __init__(self, website, username, password):
        """
        Initialize a new PasswordEntry object.
        
        Args:
            website (str): The website or service name
            username (str): The username for the service
            password (str): The password for the service
        """
        self.website = website
        self.username = username
        self.password = password
    
    def get_website(self):
        """Return the website/service name."""
        return self.website
    
    def get_username(self):
        """Return the username."""
        return self.username
    
    def get_password(self):
        """Return the password."""
        return self.password
    
    def set_website(self, website):
        """Set the website/service name."""
        self.website = website
    
    def set_username(self, username):
        """Set the username."""
        self.username = username
    
    def set_password(self, password):
        """Set the password."""
        self.password = password
    
    def to_dict(self):
        """
        Convert the entry to a dictionary format for serialization.
        
        Returns:
            dict: The entry as a dictionary
        """
        return {
            'website': self.website,
            'username': self.username,
            'password': self.password
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a PasswordEntry object from a dictionary.
        
        Args:
            data (dict): Dictionary containing entry data
            
        Returns:
            PasswordEntry: A new PasswordEntry object
        """
        return cls(
            website=data.get('website'),
            username=data.get('username'),
            password=data.get('password')
        )
    
    def __str__(self):
        """Return a string representation of the entry."""
        return f"Website: {self.website}, Username: {self.username}"
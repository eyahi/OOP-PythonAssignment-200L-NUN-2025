#the main file that runs the program

#PasswordEntry test
from password_entry import PasswordEntry

def password_entry():
    entry = PasswordEntry("github.com", "zlea-joycrate", "Firstclass5.0")
    print(entry.to_dict()) #prints the dictionary version

     # Save the entry to a file
    data = entry.to_dict()
    loaded_entry = PasswordEntry.from_dict(data) 
    print(loaded_entry.website, loaded_entry.username, loaded_entry.password) #prints the loaded entry

if __name__ == "__main__":
    password_entry()

#Encryption test
from encryption_util import EncryptionUtil
def test_encryption():
    text = "Firstclass5.0"
    encrypted = EncryptionUtil.encrypt(text)
    print ("Encrypted:", encrypted)

    decrypted = EncryptionUtil.decrypt(encrypted)
    print ("Decrypted:", decrypted)

if __name__ == "__main__":
    test_encryption()

#PasswordManager test
from password_entry import PasswordEntry
from password_manager import PasswordManager

def password_manager():
    manager = PasswordManager()

    #Adding a new password
    entry = PasswordEntry("Amazon.com", "anuri_mena", "welov3shopp1ng")
    manager.add_password(entry)

    entry = PasswordEntry("github.com", "zlea-joycrates", "Firstclass5.0")
    manager.add_password(entry)

    #getting the password
    result = manager.get_password("Amazon.com")
    if result:
        print(f"Found: {result.website} - {result.username} - {result.password}")
    else:
        print("Not found")

    result = manager.get_password("github.com")
    if result:
        print(f"Found: {result.website} - {result.username} - {result.password}")
    else:
        print("Not found")

    result = manager.get_password("google.com")
    if result:
        print(f"Found: {result.website} - {result.username} - {result.password}")
    else:
        print("Not found")

    print("Updating password for Amazon.com")
    updated = manager.update_password("Amazon.com", "anuri_mena_updated", "w3lovecloth3s")
    if updated:
        print("Update successful.")
    else:
        print("Update failed.")

    #get again to confirm update
    print("Getting updated password...")
    found = manager.get_password("Amazon.com")
    if found:
        print(f"Updated: {found.website}, {found.username}, {found.password}")

    #Delete the entry
    print("Deleting password entry...")
    manager.delete_password("Amazon.com")
    print("Deleted.")

    #Try to retrieve deleted entry
    print("Trying to retrieve deleted entry...")
    found = manager.get_password("Amazon.com")
    if found:
        print("ERROR: Entry still exists!")
    else:
        print("Entry deleted successfully.")

if __name__ == "__main__":
    password_manager()
    

from ui import main

# Run the GUI app
if __name__ == "__main__":
    main()
# This will start the GUI application
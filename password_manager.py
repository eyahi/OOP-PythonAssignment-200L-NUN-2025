from hash_maker import get_secret_key  # Since you've implemented it there
from menu import menu, create, find, find_accounts

# Main authentication
secret = get_secret_key()
passw = input('Please provide the master password to start using benard868: ')

if passw == secret:
    print('logged in successfully')
else:
    print('Incorrect password. Access denied.')
    exit()

# Main program loop
while True:
    choice = menu().upper()  # Convert to uppercase to handle 'q' or 'Q'

    if choice == 'Q':
        print("HAVE A NICE DAY!")
        break
    elif choice == '1':
        create()
    elif choice == '2':
        find_accounts()
    elif choice == '3':
        find()
    else:
        print("Invalid choice. Please select 1, 2, 3, or Q.")
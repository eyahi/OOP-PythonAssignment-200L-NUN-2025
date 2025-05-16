import sqlite3
from cryptography.fernet import Fernet


class DbOperations:

    def __init__(self):
        self.key = self.load_key()
        self.fernet = Fernet(self.key)

    def load_key(self):
        try:
            with open("secret.key", "rb") as f:
                return f.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open("secret.key", "wb") as f:
                f.write(key)
            return key

    def connect_to_db(self):
        conn = sqlite3.connect('password_records.db')
        return conn

    def create_table(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            website TEXT NOT NULL,
            username VARCHAR(200),
            password TEXT
        );
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def create_record(self, data, table_name="password_info"):
        website = data['website']
        username = data['username']
        password = self.fernet.encrypt(data['password'].encode())  #Encrypt password
        conn = self.connect_to_db()
        query = f'''
        INSERT INTO {table_name} (website, username, password) VALUES (?, ?, ?);
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username, password))

    def show_records(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name};
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_records = cursor.execute(query).fetchall()

            decrypted_records = []
            for row in list_records:
                decrypted_password = self.fernet.decrypt(row[5]).decode()
                # row: (ID, created_date, update_date, website, username, password)
                decrypted_records.append((
                    row[0],  # ID
                    row[1],  # created_date
                    row[2],  # update_date
                    row[3],  # website
                    row[4],  # username
                    decrypted_password  # decrypted password
                ))
            return decrypted_records

    def update_record(self, data, table_name="password_info"):
        ID = data['ID']
        website = data['website']
        username = data['username']
        password = self.fernet.encrypt(data['password'].encode())  #Encrypt updated password
        conn = self.connect_to_db()
        query = f'''
        UPDATE {table_name} SET website = ?, username = ?, password = ? WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username, password, ID))

    def delete_record(self, ID, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        DELETE FROM {table_name} WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ID,))

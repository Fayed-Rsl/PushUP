from datetime import date
import sqlite3

from sqlite3 import Error as SqlError

class Database:
    def __init__(self, path):
        '''Connect to the database'''
        self.conn = self.connection(path)
        self.cursor = self.conn.cursor()

    def connection(self, path):
        '''connect to SQL lite database'''
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
            return connection
        except SqlError as e:
            print(f"Error ID: Connection. The error '{e}' occurred")

    def drop_table(self, table:str):
        '''name of the table
        table:str
        '''
        try:
            self.cursor.execute("DROP TABLE IF EXISTS" + ' ' + table)
            self.conn.commit()
            print(f'Dropped table {table}' )
        except SqlError as e:
            print(f"Error ID: Drop Table. The error '{e}' occurred")

    def create_user_table(self):
        '''create user table
        username:str (unique)
        password:str
        email:str (unique)
        timestamp:date'''
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS _User
                    (username CHAR(20) NOT NULL UNIQUE,
                    password CHAR(50) NOT NULL,
                    email CHAR(255) NOT NULL UNIQUE,
                    timestamp DATE NOT NULL)''')
            self.conn.commit()
            print(f'User Table successfully created.')
        except SqlError as e:
            print(f"Error ID: Create _User. The error '{e}' occurred")

    def create_user_goal(self):
        '''create user goal table and how long to achieve the goal
        user_id:rowid of user'''
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS _UserGoal
                    (user_id INT NOT NULL PRIMARY KEY UNIQUE,
                    push_up INT NOT NULL,
                    push_up_time DATE NOT NULL,
                    pull_up INT NOT NULL,
                    pull_up_time DATE NOT NULL,
                    abdo INT NOT NULL,
                    abdo_time DATE NOT NULL,
                    squat INT NOT NULL,
                    squat_time DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES _User (user_id))''')
            self.conn.commit()
            print(f'UserGoal Table successfully created.')
        except SqlError as e:
            print(f"Error ID: Create _UserGoal. The error '{e}' occurred")

    def create_userdata_table(self):
        '''create userdata table that will store every data of users
        user_id:rowid of user
        '''
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS _UserData
                    (user_id INT NOT NULL,
                    push_up INT NOT NULL,
                    pull_up INT NOT NULL,
                    abdo INT NOT NULL,
                    squat INT NOT NULL,
                    day DATE NOT NULL,
                    PRIMARY KEY (USER_ID, DAY),
                    FOREIGN KEY (user_id) REFERENCES _User (user_id))''') # composite key: USER_ID + DAY
            self.conn.commit()
            print(f'User DataTable successfully created.')

        except SqlError as e:
            print(f"Error ID: Create _UserData. The error '{e}' occurred")

    def insert_user(self, value:tuple):
        '''insert new user in the _User table
        value:tuple (username, password, email, timestamp)'''
        try:
            self.cursor.execute('''INSERT INTO _User (username, password, email, timestamp)
            VALUES (?, ?, ?, ?)''', value)
            self.conn.commit()
            print(f'User {value} successfully inserted in Database.')
            return self.cursor.lastrowid
        except SqlError as e:
            print(f"Error ID: Insert User. The error '{e}' occurred")

    def insert_goal(self, value:tuple):
        '''insert goal user in the _UserGoal table
        value:tuple (user_id, push_up, push_up_time, pull_up, pull_up_time,
        abdo, abdo_time, squat, squat_time)'''
        try:
            self.cursor.execute('''INSERT INTO _UserGoal (user_id, push_up,
            push_up_time, pull_up, pull_up_time, abdo, abdo_time, squat, squat_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''', value)
            self.conn.commit()
            print(f'UserGoal {value} successfully inserted in Database.')
        except SqlError as e:
            print(f"Error ID: Insert Goal. The error '{e}' occurred")

    def insert_data(self, value:tuple):
        '''insert new userdata in the _UserData table
        value:tuple (user_id, push_up, pull_up, abdo, squat, day)'''

        try:
            self.cursor.execute('''INSERT INTO _UserData (user_id, push_up, pull_up, abdo, squat, day)
            VALUES (?, ?, ?, ?, ?, ?)''', value)
            self.conn.commit()
            print(f'UserData successfully inserted in Database.')
        except SqlError as e:
            print(f"Error ID: Insert Data. The error '{e}' occurred")
            
    def update_data(self, value:tuple):
        '''update userdata in the _UserData table
        value:tuple (push_up, pull_up, abdo, squat, user_id, day)'''

        try:
            self.cursor.execute('''UPDATE _UserData
            SET push_up = ?, pull_up = ?, abdo = ?, squat = ?
            WHERE user_id = ? AND day = ?''', value)
            self.conn.commit()
            print(f'UserData {value} successfully updated in Database.')
        except SqlError as e:
            print(f"Error ID: Update Data. The error '{e}' occurred")

    def get_user_id(self, value:tuple):
        '''get the user id
        value:tuple (username, email)
        return: integer (user rowid)'''
        try:
            self.cursor.execute('''SELECT rowid FROM _User WHERE email = ? ''', value)
            USER_ID = self.cursor.fetchone()[0]
            print(f'User rowid: {USER_ID}')
            return USER_ID
        except SqlError as e:
            print(f"Error ID: Get UserID. The error '{e}' occurred")

    def check_user_goal(self, value:tuple):
        '''check if user already have a goal
        value:tuple (user_id)
        return:bool 1 or 0'''
        try:
            self.cursor.execute('''SELECT * FROM _UserGoal WHERE user_id = ? ''', value)
            CHECK = self.cursor.fetchone()
            
            # if user has a goal return 1
            if CHECK != None: return 1
            else: return 0 
        except SqlError as e:
            print(f"Error ID: Check Goal. The error '{e}' occurred")

    def check_primary_key(self, value:tuple):
        '''check if user already entered data today.
        value:tuple (user_id, day)
        return:bool 1 or 0'''
        try:
            self.cursor.execute('''SELECT user_id, day FROM _UserData WHERE user_id = ? AND day = ? ''', value)
            CHECK = self.cursor.fetchone()

            # if user didnt entered data today return 1
            if CHECK != None: return 1
            else: return 0 
        except SqlError as e:
            print(f"Error ID: Check PK. The error '{e}' occurred")        

    def check_account(self, value:tuple):
        '''check if the account exist and if correct password
        value:tuple (email, password)
        return 1 or 0'''
        try:
            self.cursor.execute('''SELECT email, password FROM _User WHERE email = ? AND password = ? ''', value)
            CHECK = self.cursor.fetchone()

            # if email and password does not exist return 1
            if CHECK != None: return 1
            else: return 0 
        except SqlError as e:
            print(f"Error ID: Check Account. The error '{e}' occurred")        

    @staticmethod
    def get_date():
        '''function to get today date'''
        return date.today().strftime('%Y-%m-%d')


#load data
# df = pandas.read_csv(csvfile)
# df.to_sql('nom de ma table', conn, if_exists='append', index=False)
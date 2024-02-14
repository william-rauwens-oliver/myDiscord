import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="willy",
            database="discord"
        )
        self.cursor = self.db.cursor()

    def check_login(self, email, password):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        self.cursor.execute(query, (email, password))
        result = self.cursor.fetchone()
        return result is not None

    def insert_user(self, name, first_name, email, password):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, first_name, email, password))
        self.db.commit()
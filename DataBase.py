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
        check_query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(check_query, (email,))
        existing_user = self.cursor.fetchone()
        
        if existing_user:
            print("L'e-mail existe déjà dans la base de données.")
            return False
        else:
            query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (name, first_name, email, password))
            self.db.commit()
            print("Utilisateur inséré avec succès dans la base de données.")
            return True
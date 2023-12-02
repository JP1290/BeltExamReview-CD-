from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db = 'recipes'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_users(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be longer than 2 character(s).", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be longer than 2 character(s).", "register")
            is_valid = False
        if len(user["email"]) < 3:
            flash("E-mail must be longer than 3 character(s).", "register")
            is_valid = False
        if len(user['password']) < 7:
            flash("Passwords must be 8 characters or longer.", "register")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def save_users(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_emails(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
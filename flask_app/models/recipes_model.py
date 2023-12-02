from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask import render_template, redirect, request, session, flash


db = 'recipes'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.thirty_minutes = data['thirty_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.posted_by = []

    @staticmethod
    def validate_recipes(user):
        is_valid = True
        if len(user['name']) < 3:
            flash("Name must be longer than 3 character(s).")
            is_valid = False
        if len(user['description']) < 3:
            flash("Description must be longer than 3 character(s).")
            is_valid = False
        if len(user['instruction']) < 3:
            flash("Instructions must be longer than 3 character(s).")
            is_valid = False
        if user['date_cooked'] == "":
            flash("Date must not be empty.")
            is_valid = False
        if user['thirty_minutes'] == "":
            flash("Select an option for Thirty Minutes.")
            is_valid = False
        return is_valid

    @classmethod
    def get_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_recipes_by_user(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        result = connectToMySQL(db).query_db(query)
        user_recipes = []
        for recipe in result:
            user_recipe = cls(recipe)
            user_recipe_info = {
                'id': recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            user_recipe.posted_by.append(users_model.User(recipe))
            user_recipes.append(user_recipe)
        return user_recipes
    
    @classmethod
    def get_recipes_by_userid(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        user_recipes = []
        for recipe in result:
            user_recipe = cls(recipe)
            user_recipe_info = {
                'id': recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            user_recipe.posted_by.append(users_model.User(recipe))
            user_recipes.append(user_recipe)
        return user_recipes
    
    @classmethod
    def save_recipes(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, date_cooked, thirty_minutes, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(date_cooked)s, %(thirty_minutes)s, %(id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def update_recipes(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, date_cooked = %(date_cooked)s, thirty_minutes = %(thirty_minutes)s WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def delete_recipes(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes')
def user_recipes():
    return render_template('usersrecipes.html', user_id = session['user_id'], recipes = Recipe.get_recipes_by_user(), first_name = session['user'])

@app.route('/recipes/new')
def new_recipes():
    return render_template('newrecipes.html')

@app.route('/recipes/create', methods = ['POST'])
def create_recipes():    
    if not Recipe.validate_recipes(request.form):
        return redirect('/recipes/new')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'date_cooked': request.form['date_cooked'],
        'thirty_minutes': request.form['thirty_minutes'],
        'id': session['user_id']
    }

    Recipe.save_recipes(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def specific_recipe(id):
    data = {
        'id': id
    }
    return render_template('recipes.html', recipes = Recipe.get_recipes_by_userid(data), first_name = session['user'])

@app.route('/recipes/edit/<int:id>')
def edit_recipes(id):
    session['idr'] = id
    data = {
        'id': id
    }
    return render_template('editrecipes.html', recipes = Recipe.get_recipes_by_userid(data))

@app.route('/edit', methods = ['POST'])
def editing():
    if not Recipe.validate_recipes(request.form):
        return redirect('/recipes/edit/' + str(session['idr']))
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'date_cooked': request.form['date_cooked'],
        'thirty_minutes': request.form['thirty_minutes'],
        'id': session['idr']
    }
    Recipe.update_recipes(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def deleting(id):
    delete_id = {
        'id': id
    }
    Recipe.delete_recipes(delete_id)
    return redirect('/recipes')
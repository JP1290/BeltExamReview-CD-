from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/') #Get request for 127.0.0.1:5000
def home():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_users(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
    "first_name": request.form['first_name'],
    "last_name": request.form['last_name'],
    "email": request.form['email'],
    "password": pw_hash
    }
    user_id = User.save_users(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    specific_user = User.get_emails(data)
    if not specific_user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(specific_user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = specific_user.id
    session['user'] = specific_user.first_name
    return redirect('/recipes')

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect('/')
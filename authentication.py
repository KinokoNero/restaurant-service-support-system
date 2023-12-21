from functools import wraps

import bcrypt
from bson import ObjectId
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from pymongo import MongoClient

from classes import User, Role

# Admin routes blueprint
auth_routes = Blueprint('auth_routes', __name__, template_folder='templates')

# Initialize database
client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]
users = db["users"]

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth_routes.admin_login'


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != required_role:
                abort(403)  # Forbidden
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt


def verify_password(password, hashed_password, salt):
    hashed_input_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_input_password == hashed_password


@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User.from_dict(user_data)


@auth_routes.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user_data = users.find_one({'name': name, 'role': 'admin'})
        correct_password = verify_password(password, user_data.get("password"), user_data.get("salt"))

        if user_data and correct_password:
            user = User.from_dict(user_data)
            login_user(user)
            flash('User logged in successfully!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    else:
        return render_template('admin_login.html')


@auth_routes.route('/login/qr', methods=['GET'])
def qr_login():
    table_id = request.args.get("table_id")
    user_data = users.find_one({'_id': ObjectId(table_id)})

    if user_data:
        user = User.from_dict(user_data)
        login_user(user)
        flash('User logged in successfully!', 'success')
        return redirect(url_for('menu'))
    else:
        flash('Login failed. User not found.', 'danger')

    return redirect(url_for('menu'))


@auth_routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session = []
    flash('User logged out successfully!', 'success')
    return redirect(url_for('menu'))


def get_current_user():
    return current_user

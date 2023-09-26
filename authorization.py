from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from pymongo import MongoClient

# Admin routes blueprint
auth_routes = Blueprint('auth_routes', __name__, template_folder='templates')

# Initialize database
client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]
users = db["users"]

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth_routes.admin_login'

@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({'_id': user_id})
    if user_data:
        return User(user_data['_id'], user_data['username'], user_data['role'])

# Define routes
@auth_routes.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.find_one({'username': username, 'password': password})
        if user_data:
            user = User(user_data['_id'], user_data['username'], user_data['role'])
            login_user(user)
            flash('Admin logged in successfully!', 'success')
            return redirect(url_for('main_page'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('admin-login.html')

@auth_routes.route('/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Admin logged out successfully!', 'success')
    return redirect(url_for('main-page'))
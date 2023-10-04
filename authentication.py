from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from bson import ObjectId
from functools import wraps
from security import verify_password

# Admin routes blueprint
auth_routes = Blueprint('auth_routes', __name__, template_folder='templates')

# Initialize database
client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]
users = db["users"]

class User(UserMixin):
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth_routes.admin_login'

@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data['_id'], user_data['name'], user_data['role'])

@auth_routes.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user_data = users.find_one({'name': name, 'role': "Admin"})
        correct_password = verify_password(password, user_data.get("password"), user_data.get("salt"))
        
        if user_data and correct_password:
            user = User(user_data['_id'], user_data['name'], user_data['role'])
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
        user = User(user_data['_id'], user_data['name'], user_data['role'])
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
    #TODO: add session clearing at logout
    flash('User logged out successfully!', 'success')
    return redirect(url_for('menu'))

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if current_user.role != required_role:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
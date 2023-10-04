from flask import Flask, render_template, session
from authentication import auth_routes, login_manager, role_required
from database import db_routes, menu_collection, users_collection
from session import session_routes
#from flask_session import Session
from flask_login import login_required

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'c9383efdbb41c23072b029ecc4789e36'
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(db_routes, url_prefix='/db')
app.register_blueprint(session_routes, url_prefix='/session')
login_manager.init_app(app)

@app.route('/menu', methods=['GET'])
@login_required
def menu():
    items = menu_collection.find()
    return render_template('menu.html', items=items)

@app.route('/table-manager', methods=['GET'])
@login_required
@role_required('Admin')
def table_manager():
    tables = users_collection.find({"role": {"$ne": "Admin"}})
    return render_template('table_manager.html', tables=tables)

@app.route('/order-manager', methods=['GET'])
@login_required
@role_required('User')
def order_manager():
    if 'order' not in session:
        session['order'] = []

    items = session['order']
    return render_template('order_manager.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
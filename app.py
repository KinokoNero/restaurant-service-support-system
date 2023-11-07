from flask import Flask, render_template, session
from authentication import auth_routes, login_manager, role_required
from database import db_routes, client, menu_collection, users_collection, orders_collection
from session import session_routes
from flask_session import Session
from flask_login import login_required

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'c9383efdbb41c23072b029ecc4789e36'

#Blueprints setup
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(db_routes, url_prefix='/db')
app.register_blueprint(session_routes, url_prefix='/session')

# Login manager setup
login_manager.init_app(app)

# Session setup
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = client
Session(app)

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

@app.route('/orders-manager', methods=['GET'])
@login_required
@role_required('Admin')
def orders_manager():
    orders = orders_collection.find()
    return render_template('orders_manager.html', orders=orders)

@app.route('/my-order', methods=['GET'])
@login_required
@role_required('User')
def my_order():
    if 'order' not in session:
        session['order'] = []

    items = session['order']
    print(session['order']) #TEST------------------------------------------------------------------------------------------------------------------------
    return render_template('my_order.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
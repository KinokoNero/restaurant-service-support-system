from flask import Flask, render_template, session
from authentication import auth_routes, login_manager, role_required
from database import db_routes, client, get_menu, get_tables
from session import session_routes, get_current_user_order_info
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
    items = get_menu()
    return render_template('menu.html', items=items)

@app.route('/table-manager', methods=['GET'])
@login_required
@role_required('Admin')
def table_manager():
    tables = get_tables()
    return render_template('table_manager.html', tables=tables)

@app.route('/orders-manager', methods=['GET'])
@login_required
@role_required('Admin')
def orders_manager():
    orders = get_orders()
    return render_template('orders_manager.html', orders=orders)

@app.route('/current-user-order', methods=['GET'])
@login_required
@role_required('User')
def current_user_order():
    order_items, order_sum = get_current_user_order_info()
    return render_template('current_user_order.html', order_items=order_items, order_sum=order_sum)

if __name__ == '__main__':
    app.run(debug=True)
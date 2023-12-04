from flask import Flask, render_template, session
from authentication import auth_routes, login_manager, role_required
from classes import Role, ServiceRequestType, service_request_type_display_strings, Status, status_display_strings
from database import db_routes, client, get_menu, get_tables, get_orders
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

# Global variables accessible in templates
app.jinja_env.globals['Role'] = Role # Role enum

@app.route('/menu', methods=['GET'])
@login_required
def menu():
    items = get_menu()
    return render_template('menu.html', items=items)

#TODO: add a view for single menu item

@app.route('/table-manager', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def table_manager():
    tables = get_tables()
    return render_template('table_manager.html', tables=tables)

@app.route('/orders-manager', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def orders_manager():
    orders = get_orders()
    return render_template('orders_manager.html', orders=orders, statuses=Status, status_display_strings=status_display_strings)

@app.route('/current-user-order', methods=['GET'])
@login_required
@role_required(Role.USER)
def current_user_order():
    order_items, price_sum = get_current_user_order_info()
    return render_template('current_user_order.html', order_items=order_items, price_sum=price_sum)

@app.route('/service-request', methods=['GET'])                             #TODO: add admin requests manager
@login_required
@role_required(Role.USER)
def service_request():
    return render_template('service_request_form.html', service_request_types=ServiceRequestType, service_request_type_display_strings=service_request_type_display_strings)

if __name__ == '__main__':
    app.run(debug=True)
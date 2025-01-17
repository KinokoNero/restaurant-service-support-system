import os

from bson import ObjectId
from flask import Blueprint, request, render_template, flash, redirect, url_for, make_response
from flask_login import login_required
from gridfs import GridFS
from pymongo import MongoClient

from authentication import role_required, load_user
from classes import Role, User, MenuItem, Order, Status, ServiceRequest
from qr import generate_qr_code

db_routes = Blueprint('db_routes', __name__, template_folder='templates')

# MongoDB configuration

client = MongoClient('mongodb://localhost:27017/r3s')
db = client['r3s']
users_collection = db['users']
menu_collection = db['menu']
orders_collection = db['orders']
requests_collection = db['requests']
fs = GridFS(db)  # For storing images


@db_routes.route('/get-image/<image_id>')
def get_image(image_id):
    image = fs.get(ObjectId(image_id))
    response = make_response(image.read())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


# Menu items
@db_routes.route('/add-item', methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        item = MenuItem(name=name, description=description, price=price)
        image = request.files['image']
        if image and image.filename != '':
            image_id = fs.put(image, filename=image.filename)
            item.image_id = image_id

        item_dict = item.to_dict()

        result = menu_collection.insert_one(item_dict)

        if result.acknowledged:
            flash('Nowe danie zostało dodane do bazy.', 'success')
        else:
            flash('Nie udało się dodać nowego dania do bazy.', 'error')

        return redirect(url_for('menu'))
    else:
        return render_template('add_item_form.html')


@db_routes.route('/modify-item/<item_id>', methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def modify_item(item_id):
    item_id = ObjectId(item_id)
    item_data = menu_collection.find_one({'_id': item_id})
    menu_item = MenuItem.from_dict(item_data)

    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']

        # Update image if selected in form
        image = request.files['image-input']
        print(image)
        if image and image.filename != '':
            if menu_item.image_id is not None:
                old_image_id = ObjectId(item_data.get('image_id'))
                fs.delete(old_image_id)
                fs.put(image, filename=image.filename, _id=old_image_id)
            else:
                image_id = fs.put(image, filename=image.filename)
                menu_item.image_id = image_id

        menu_item_dict = menu_item.to_dict()
        menu_item_dict.pop('_id')  # Remove id for update

        menu_collection.update_one({'_id': item_id}, {
            '$set': menu_item_dict
        })

        flash('Danie zostało zmodyfikowane.', 'success')

        return redirect(url_for('menu'))

    return render_template('modify_item_form.html', item=menu_item)


@db_routes.route('/delete-item-image/<item_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def delete_item_image(item_id):
    item_id = ObjectId(item_id)
    menu_item_dict = menu_collection.find_one({'_id': item_id})
    menu_item = MenuItem.from_dict(menu_item_dict)

    fs.delete(menu_item.image_id)

    menu_collection.update_one({'_id': item_id}, {
        '$unset': {'image_id': 1}
    })

    return redirect(url_for('menu'))


@db_routes.route('/delete-item/<item_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def delete_item(item_id):
    item_id = ObjectId(item_id)
    item = menu_collection.find_one({'_id': item_id})

    if item:
        image_id = item.get('image_id')
        result = menu_collection.delete_one({'_id': item_id})

        if result.deleted_count > 0:
            fs.delete(image_id)
            flash('Danie zostało usunięte.', 'success')
        else:
            flash('Nie udało się usunąć dania.', 'error')
    else:
        flash('Nie znaleziono dania.', 'error')

    return redirect(url_for('menu'))


# Tables
@db_routes.route('/add-table', methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def add_table():
    if request.method == 'POST':
        name = request.form['name']

        table = User(name=name, role=Role.USER)
        table_dict = table.to_dict()

        result = users_collection.insert_one(table_dict)

        if result.acknowledged:
            inserted_id = result.inserted_id
            qr_code_image = generate_qr_code(inserted_id)
            qr_code_image_id = fs.put(qr_code_image, filename=inserted_id)
            users_collection.update_one(
                {'_id': inserted_id},
                {'$set': {'qr_code_image_id': qr_code_image_id}}
            )

            flash('Stolik został dodany.', 'success')
        else:
            flash('Nie udało się dodać stolika.', 'error')

        return redirect(url_for('table_manager'))
    else:
        return render_template('add_table_form.html')


@db_routes.route('/modify-table/<table_id>', methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def modify_table(table_id):
    table_data = users_collection.find_one({'_id': ObjectId(table_id)})

    if request.method == 'POST':
        name = request.form['name']

        users_collection.update_one({'_id': ObjectId(table_id)}, {
            '$set': {
                'name': name
            }
        })

        flash('Stół został zmodyfikowany.', 'success')
        return redirect(url_for('table_manager'))

    return render_template('modify_table_form.html', table=table_data)


@db_routes.route('/delete-table/<table_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def delete_table(table_id):
    table_id = ObjectId(table_id)
    table = users_collection.find_one({'_id': table_id})

    if table:
        qr_code_image_id = table.get('qr_code_image_id')
        result = users_collection.delete_one({'_id': table_id})

        if result.deleted_count > 0:
            fs.delete(qr_code_image_id)
            flash('Stół został usunięty.', 'success')
        else:
            flash('Nie udało się usunąć stołu.', 'error')
    else:
        flash('Nie znaleziono stołu.', 'error')

    return redirect(url_for('table_manager'))


# Orders
@db_routes.route('/change-order-status/<order_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def change_order_status(order_id):
    order_dict = orders_collection.find_one({'_id': ObjectId(order_id)})
    order = Order.from_dict(order_dict)

    order.status = Status(request.form['status'])

    order_dict = order.to_dict()
    orders_collection.update_one({'_id': ObjectId(order_id)}, {
        '$set': order_dict
    })

    flash('Status zamówienia został zmodyfikowany.', 'success')

    return redirect(url_for('orders_manager'))


@db_routes.route('/delete-order/<order_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def delete_order(order_id):
    order_id = ObjectId(order_id)
    order = orders_collection.find_one({'_id': order_id})

    if order:
        result = orders_collection.delete_one({'_id': order_id})

        if result.deleted_count > 0:
            flash('Zamówienie zostało usunięte.', 'success')
        else:
            flash('Nie udało się usunąć zamówienia.', 'error')
    else:
        flash('Nie znaleziono zamówienia.', 'error')

    return redirect(url_for('orders_manager'))


# Service requests
@db_routes.route('/change-service-request-status/<service_request_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def change_service_request_status(service_request_id):
    service_request_dict = requests_collection.find_one({'_id': ObjectId(service_request_id)})
    service_request = ServiceRequest.from_dict(service_request_dict)

    service_request.status = Status(request.form['status'])

    service_request_dict = service_request.to_dict()
    requests_collection.update_one({'_id': ObjectId(service_request_id)}, {
        '$set': service_request_dict
    })

    flash('Status prośby został zmodyfikowany.', 'success')

    return redirect(url_for('service_requests_manager'))


@db_routes.route('/delete-service-request/<service_request_id>', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
def delete_service_request(service_request_id):
    service_request_id = ObjectId(service_request_id)
    service_request = requests_collection.find_one({'_id': service_request_id})

    if service_request:
        result = requests_collection.delete_one({'_id': service_request_id})

        if result.deleted_count > 0:
            flash('Prośba została usunięta.', 'success')
        else:
            flash('Nie udało się usunąć prośby.', 'error')
    else:
        flash('Nie znaleziono prośby.', 'error')

    return redirect(url_for('service_requests_manager'))


# Helper methods
def get_menu():
    menu_dict = menu_collection.find()
    menu = []
    for menu_item_dict in menu_dict:
        menu_item = MenuItem.from_dict(menu_item_dict)
        menu.append(menu_item)

    return menu


def get_menu_item(item_id):
    menu_item_dict = menu_collection.find_one({'_id': ObjectId(item_id)})
    menu_item = MenuItem.from_dict(menu_item_dict)
    return menu_item


def get_user(user_id):
    return load_user(user_id)


def get_tables():
    tables_dict = users_collection.find({"role": {"$ne": "admin"}})
    tables = []
    for table_dict in tables_dict:
        tables.append(User.from_dict(table_dict))

    return tables


def get_orders(include_finished=False):
    orders_dict = orders_collection.find()
    orders = []
    for order_dict in orders_dict:
        order = Order.from_dict(order_dict)

        if not include_finished and order.status == Status.FINISHED:
            continue

        for order_item in order.order_items:
            order.price_sum = order.price_sum + order_item.menu_item.price
        order.price_sum = round(order.price_sum, 2)

        orders.append(order)

    return orders


def get_service_requests(include_finished=False):
    service_requests_dict = requests_collection.find()
    service_requests = []
    for service_request_dict in service_requests_dict:
        service_request = ServiceRequest.from_dict(service_request_dict)

        if not include_finished and service_request.status == Status.FINISHED:
            continue

        service_requests.append(service_request)

    return service_requests


def insert_order(order):
    order_dict = order.to_dict()
    result = orders_collection.insert_one(order_dict)
    if result.acknowledged:
        return True
    else:
        return False


def insert_service_request(service_request):
    service_request_dict = service_request.to_dict()
    result = requests_collection.insert_one(service_request_dict)
    if result.acknowledged:
        flash('Prośba została wysłana do obsługi.', 'success')
    else:
        flash('Nie udało się wysłać prośby do obsługi.', 'error')

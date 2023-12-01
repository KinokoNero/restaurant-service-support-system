from flask import Blueprint, request, render_template, flash, redirect, url_for, make_response
from pymongo import MongoClient
from flask_login import login_required, current_user
from authentication import role_required
from classes import MenuItem
from qr import qr_codes_directory, generate_qr_code
from gridfs import GridFS
from bson import json_util, ObjectId
from flask_session import Session
import os
import json

db_routes = Blueprint('db_routes', __name__, template_folder='templates')

# MongoDB configuration
mongodb_connection_uri = "mongodb://localhost:27017/r3s"
client = MongoClient(mongodb_connection_uri)
db = client["r3s"]
users_collection = db["users"]
menu_collection = db["menu"]
orders_collection = db["orders"]
fs = GridFS(db) # For storing images

@db_routes.route('/get-image/<image_id>')
def get_image(image_id):
    image = fs.get(ObjectId(image_id))
    response = make_response(image.read())
    response.headers['Content-Type'] = 'image/jpeg'
    return response

### Menu items ###
@db_routes.route('/add-item', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']
        image_id = fs.put(image, filename=image.filename)

        item = MenuItem(name, description, price, image_id)
        item_dict = item.to_dict()

        result = menu_collection.insert_one(item_dict)

        if result.acknowledged:
            flash('Item added successfully!', 'success')
        else:
            flash('Failed to add item.', 'danger')

        return redirect(url_for('menu'))
    else:
        return render_template('add_item_form.html')

@db_routes.route('/modify-item/<item_id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def modify_item(item_id):
    item_id = ObjectId(item_id)
    item_data = menu_collection.find_one({'_id': item_id})
    
    if request.method == 'POST':
        menu_item = MenuItem.from_dict(item_data)

        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']
        
        menu_item_dict = menu_item.to_dict()
        menu_item_dict.pop('_id') # Remove id for update
        
        menu_collection.update_one({'_id': item_id}, {
            '$set': menu_item_dict
        })

        # Update image if selected in form
        image = request.files['image']
        if image and image.filename != '':
            old_image_id = ObjectId(item_data.get("image_id"))
            fs.delete(old_image_id)
            fs.put(image, filename=image.filename, _id=old_image_id)

        flash('Item modified successfully!', 'success')
        return redirect(url_for('menu'))
    
    return render_template('modify_item_form.html', item=item_data)

@db_routes.route('/delete-item/<item_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_item(item_id):
    item_id = ObjectId(item_id)
    item = menu_collection.find_one({'_id': item_id})

    if item:
        image_id = item.get('image_id')
        result = menu_collection.delete_one({'_id': item_id})

        if result.deleted_count > 0:
            fs.delete(image_id)
            flash('Item deleted successfully!', 'success')
        else:
            flash('Item could not be deleted.', 'danger')
    else:
        flash('Item not found.', 'danger')

    return redirect(url_for('menu'))

### Tables ###
@db_routes.route('/add-table', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def add_table():
    if request.method == 'POST':
        name = request.form['name'] #TODO: add user class and change methods like for menu items
        role = 'User'

        table_document = {
            'name': name,
            'role': role
        }

        result = users_collection.insert_one(table_document)

        if result.acknowledged:
            inserted_id = result.inserted_id
            qr_code_image = generate_qr_code(inserted_id)
            qr_code_image_id = fs.put(qr_code_image, filename=inserted_id)
            users_collection.update_one(
                {'_id': inserted_id},
                {'$set': {'qr_code_image_id': qr_code_image_id}}
            )
            flash('Table added successfully!', 'success')
        else:
            flash('Failed to add table.', 'danger')

        return redirect(url_for('table_manager'))
    else:
        return render_template('add_table_form.html')

@db_routes.route('/modify-table/<table_id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def modify_table(table_id):
    table_data = users_collection.find_one({'_id': ObjectId(table_id)})
    
    if request.method == 'POST':
        name = request.form['name']

        users_collection.update_one({'_id': ObjectId(table_id)}, {
            '$set': {
                'name': name
            }
        })

        flash('Table modified successfully!', 'success')
        return redirect(url_for('table_manager'))
    
    return render_template('modify_table_form.html', table=table_data)

@db_routes.route('/delete-table/<table_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_table(table_id):
    table_id = ObjectId(table_id)
    table = users_collection.find_one({'_id': table_id})

    if table:
        qr_code_image_id = table.get('qr_code_image_id')
        result = users_collection.delete_one({'_id': table_id})

        if result.deleted_count > 0:
            fs.delete(qr_code_image_id)
            file_path = f"{qr_codes_directory}/{table_id}.png"
            if os.path.exists(file_path):
                os.remove(file_path)
            flash('Table deleted successfully!', 'success')
        else:
            flash('Table could not be deleted.', 'danger')
    else:
        flash('Table not found.', 'danger')

    return redirect(url_for('table_manager'))

### Order ###
@db_routes.route('/place-order', methods=['POST'])
@login_required
@role_required('User')
def submit_order():
    if 'order' in session:
        order = session['order']
        print(order)


### Helper methods ###
def get_menu():
    return menu_collection.find()

def get_tables():
    return users_collection.find({"role": {"$ne": "Admin"}})

def get_orders():
    return orders_collection.find()

def get_menu_item(item_id):
    menu_item_dict = menu_collection.find_one({'_id': ObjectId(item_id)})
    menu_item = MenuItem.from_dict(menu_item_dict)
    return menu_item
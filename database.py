from flask import Blueprint, request, render_template, flash, redirect, url_for, make_response
from pymongo import MongoClient
from flask_login import login_required, current_user
from authentication import role_required
from qr import qr_codes_directory, generate_qr_code
from gridfs import GridFS
from bson import ObjectId
import os

db_routes = Blueprint('db_routes', __name__, template_folder='templates')

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
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

        item_document = {
            'name': name,
            'description': description,
            'price': float(price),
            'image_id': image_id
        }

        result = menu_collection.insert_one(item_document)

        if result.acknowledged:
            flash('Item added successfully!', 'success')
        else:
            flash('Failed to add item.', 'danger')

        return redirect(url_for('main_page'))
    else:
        return render_template('add_item_form.html')

@db_routes.route('/modify-item/<item_id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def modify_item(item_id):
    item_data = menu_collection.find_one({'_id': ObjectId(item_id)})
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        menu_collection.update_one({'_id': ObjectId(item_id)}, {
            '$set': {
                'name': name,
                'description': description,
                'price': price
            }
        })

        # Update image if selected in form
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                old_image_id = ObjectId(item_data.get("image_id"))
                fs.delete(old_image_id)
                fs.put(image, filename=image.filename, _id=old_image_id)

        flash('Item modified successfully!', 'success')
        return redirect(url_for('main_page'))
    
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

    return redirect(url_for('main_page'))

### Tables ###
@db_routes.route('/table-manager', methods=['GET'])
@login_required
@role_required('Admin')
def table_manager():
    tables = users_collection.find({"role": {"$ne": "Admin"}})
    return render_template('table_manager.html', tables=tables)

@db_routes.route('/add-table', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def add_table():
    if request.method == 'POST':
        name = request.form['name']
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

        return redirect(url_for('db_routes.table_manager'))
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
        return redirect(url_for('db_routes.table_manager'))
    
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

    return redirect(url_for('db_routes.table_manager'))

### Orders ###
@db_routes.route('/order-manager', methods=['GET'])
#@login_required
#@role_required('Admin')
def order_manager():
    orders = users_collection.find({"role": {"$ne": "Admin"}})
    return render_template('table_manager.html', tables=tables)
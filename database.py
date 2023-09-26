from flask import Blueprint
from pymongo import MongoClient
from flask_login import login_required, current_user
from authorization import role_required

db_routes = Blueprint('database', __name__, template_folder='templates')

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]
users = db["users"]
menu = db["menu"]
orders = db["orders"]

@db_routes.route('/add-item', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        # Process and store the image file if needed
        image = request.files['image']

        item_document = {
            'name': name,
            'description': description,
            'price': float(price),
            'image_path': None  # TODO: Store the image path or GridFS file ID
        }

        result = menu.insert_one(item_document)

        if result.acknowledged:
            flash('Item added successfully!', 'success')
        else:
            flash('Failed to add item.', 'danger')

        return redirect(url_for('main_page'))
    else:
        return render_template('add_item_form.html')

# TODO: add delete and modify methods
from flask_session import Session
from bson import ObjectId
from database import menu_collection

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

class OrderItem:
    def __init__(self, menu_item, additional_info=""):
        self.menu_item = menu_item
        self.additional_info = additional_info

"""class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        # Check if the same item already exists in the order and if so, update its quantity
        for existing_item in self.items:
            if existing_item.menu_item['_id'] == item.menu_item['_id'] and existing_item.additional_info == item.additional_info:
                existing_item.quantity += item.quantity
                return
        self.items.append(item)

    def remove_item(self, item_index):
        for item in self.items:
            #TODO: removing by button

    def decrease_quantity(self, item_index):
        #TODO: decrease quantity and remove if quantity==0

    def total_price(self):
        return sum(item.subtotal() for item in self.items)

    def clear_order(self):
        self.items = []

    def __str__(self):
        order_str = ""
        for item in self.items:
            menu_item = item.menu_item
            order_str += f"{menu_item['name']} ({item.additional_info}): {item.quantity} x ${menu_item['price']} each = ${item.subtotal()}\n"
        order_str += f"Total: ${self.total_price()}"
        return order_str"""

@app.route('/add-to-order/<item_id>')
def add_to_order(item_id):
    item = menu_collection.find_one({'_id': ObjectId(item_id)})
    additional_info = request.form['additional-info']

    # Initialize order for session
    if 'order' not in session:
        session['order'] = []

    order_item = OrderItem(item, additional_info)
    
    session['order'].append(order_item)

    #TODO: redirect to different pages based on where the request was sent from (from main page or from order manager)
    return redirect(url_for('main_page'))
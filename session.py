from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from bson import ObjectId
from database import menu_collection
import json

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

class OrderItem:
    def __init__(self, menu_item, additional_info=""):
        self.menu_item = menu_item
        self.additional_info = additional_info

    def to_dict(self):
        return {
            'menu_item': self.serialize_menu_item(self.menu_item),
            'additional_info': self.additional_info
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['menu_item'], data.get('additional_info', ""))

    def serialize_menu_item(self, menu_item):
        serialized_menu_item = {}

        for key, value in menu_item.items():
            if isinstance(value, ObjectId):
                serialized_menu_item[key] = str(value)
            else:
                serialized_menu_item[key] = value

        return serialized_menu_item

@session_routes.route('/add-to-order/<item_id>', methods=['POST'])
def add_to_order(item_id):
    item = menu_collection.find_one({'_id': ObjectId(item_id)})

    if 'order' not in session:
        session['order'] = []

    order_item = OrderItem(item)
    serialized_order_item = json.dumps(order_item.to_dict())
    session['order'].append(serialized_order_item)

    # Check the source of the request
    source = request.args.get('source')
    if source == 'order_manager':
        return redirect(url_for('order_manager'))
    else:
        return redirect(url_for('menu'))

@session_routes.route('/remove-from-order/<item_index>', methods=['POST'])
def remove_from_order(item_index):
    if 'order' in session:
        order = session['order']

        if 0 <= int(item_index) < len(order):
            order.pop(int(item_index))

        session['order'] = order

    return redirect(url_for('order_manager'))
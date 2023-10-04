from flask import Blueprint, request, render_template, redirect, url_for, flash, session
#from flask_session import Session
from bson import ObjectId
from database import menu_collection

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

class OrderItem:
    def __init__(self, menu_item, additional_info=""):
        self.menu_item = menu_item
        self.additional_info = additional_info

@session_routes.route('/add-to-order/<item_id>', methods=['POST'])
def add_to_order(item_id):
    item = menu_collection.find_one({'_id': ObjectId(item_id)})

    # Initialize order for session
    if 'order' not in session:
        session['order'] = []

    order_item = OrderItem(item)
    
    session['order'].append(order_item) #TODO: implement proper flask session because this doesn't persist between requests

    # Check the source of the request
    source = request.args.get('source')
    if source == 'order_manager':
        return redirect(url_for('order_manager'))
    else:
        return redirect(url_for('menu'))

@session_routes.route('/remove-from-order/<item_index>')
def remove_from_order(item_index):
    if 'order' in session:
        order = session['order']

        if 0 <= item_index < len(order):
            order.pop(item_index)

    return redirect(url_for('order_manager'))
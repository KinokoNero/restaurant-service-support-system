from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from bson import ObjectId
from database import get_menu_item
import json

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

@session_routes.route('/add-to-order/<item_id>', methods=['POST'])
@login_required
@role_required('User')
def add_to_order(item_id):
    if 'order' not in session:
        session['order'] = []

    order_item = {
        "item_id": item_id,
        "count": 1,
        "additional_info": ""
    }
    session['order'].append(order_item)

    # Check the source of the request
    source = request.args.get('source')
    if source == 'order_manager':
        return redirect(url_for('order_manager'))
    else:
        return redirect(url_for('menu'))

@session_routes.route('/remove-from-order/<item_index>', methods=['POST'])
@login_required
@role_required('User')
def remove_from_order(item_index):
    if 'order' in session:
        order = session['order']

        if 0 <= int(item_index) < len(order):
            order.pop(int(item_index))

        session['order'] = order

    return redirect(url_for('current_user_order'))

@session_routes.route('/update-order-item/<item_index>', methods=['POST'])
@login_required
@role_required('User')
def update_order_item(item_index, new_item_data):
    #TODO


def get_current_user_order_info():
    if 'order' not in session:
        session['order'] = []

    order_items = []
    order_sum = 0

    for order_item in session['order']:
        menu_item = get_menu_item(order_item.get("item_id"))

        if menu_item:
            item_count = order_item.get("count")
            additional_item_info = order_item.get("additional_info")
            item_price = menu_item.get("price")

            order_items.append({'menu_item': menu_item, 'count': item_count, 'additional_info': additional_item_info})
            order_sum = order_sum + item_price

    return order_items, order_sum
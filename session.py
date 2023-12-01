from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from bson import ObjectId
from database import get_menu_item, submit_order
from classes import Role, MenuItem, OrderItem
from authentication import login_required, role_required
import json

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

@session_routes.route('/add-to-order/<item_id>', methods=['POST'])
@login_required
@role_required(Role.USER)
def add_to_order(item_id):
    if 'order' not in session:
        session['order'] = []

    menu_item = get_menu_item(item_id)
    order_item = OrderItem(menu_item=menu_item, count=1, additional_info="")
    order_item_dict = order_item.to_dict()

    session['order'].append(order_item_dict)

    # Check the source of the request
    source = request.args.get('source')
    if source == 'current_user_order':
        return redirect(url_for('current_user_order'))
    else:
        return redirect(url_for('menu'))

@session_routes.route('/remove-from-order/<item_index>', methods=['POST'])
@login_required
@role_required(Role.USER)
def remove_from_order(item_index):
    if 'order' in session:
        order = session['order']

        if 0 <= int(item_index) < len(order):
            order.pop(int(item_index))

        session['order'] = order

    return redirect(url_for('current_user_order'))

@session_routes.route('/update-order-item/<item_index>', methods=['POST'])
@login_required
@role_required(Role.USER)
def update_order_item(item_index):
    item_index = int(item_index)

    if 'order' in session:
        order = session['order']
        order_item_dict = order[item_index]
        order_item = OrderItem.from_dict(order_item_dict)

        order_item.count = request.form['item-count']
        order_item.additional_info = request.form['additional-info']

        order_item_dict = order_item.to_dict()
        session['order'][item_index] = order_item_dict

    return redirect(url_for('current_user_order'))

def get_current_user_order_info():
    if 'order' not in session:
        session['order'] = []

    order_items = []
    order_sum = 0

    for order_item_dict in session['order']:
        order_item = OrderItem.from_dict(order_item_dict)
        order_items.append(order_item)
        
        order_sum = order_sum + order_item.menu_item.price * order_item.count
        order_sum = round(order_sum, 2)

    return order_items, order_sum

@session_routes.route('/place-order', methods=['POST'])
@login_required
@role_required(Role.USER)
def place_order():
    if 'order' in session:
        order = session['order']

        if order:
            submit_order(order)
            session['order'] = []
    
    return redirect(url_for('menu'))
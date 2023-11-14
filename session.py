from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from bson import ObjectId
from database import get_menu_item
from authentication import login_required, role_required
import json

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

class OrderItem:
    def __init__(self, menu_item_id, count, additional_info):
        self.menu_item_id = menu_item_id
        self.count = count
        self.additional_info = additional_info

    def to_dict(self):
        order_item = {
            'menu_item_id': ObjectId(self.menu_item_id),
            'count': int(self.count),
            'additional_info': self.additional_info,
        }
        return order_item

    @classmethod
    def from_dict(cls, order_item_dict):
        return cls(
            item_id=ObjectId(order_item_dict['menu_item_id']),
            count=int(order_item_dict['count']),
            additional_info=order_item_dict['additional_info'],
        )

@session_routes.route('/add-to-order/<item_id>', methods=['POST'])
@login_required
@role_required('User')
def add_to_order(item_id):
    if 'order' not in session:
        session['order'] = []

    order_item = OrderItem(menu_item_id=item_id, count=1, additional_info="")
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
def update_order_item(item_index): #TODO: test updating the order item by count and additional info
    if 'order' in session:
        order = session['order']
        order_item = order[item_index]

        menu_item_id = order_item['menu_item_id']
        item_count = request.form['item-count']
        additional_info = request.form['additional-info']

        updated_order_item = OrderItem(menu_item_id, item_count, additional_info)
        updated_order_item_dict = updated_order_item.to_dict()

        session['order'][item_index] = updated_order_item_dict

    return redirect(url_for('current_user_order'))

def get_current_user_order_info(): #TODO: implement OrderItem and MenuItem(?) object in this method
    if 'order' not in session:
        session['order'] = []

    order_items = []
    order_sum = 0

    for order_item in session['order']:
        menu_item = get_menu_item(order_item.get("menu_item_id"))

        if menu_item:
            item_count = order_item.get("count")
            additional_item_info = order_item.get("additional_info")
            item_price = menu_item.get("price")

            order_items.append({'menu_item': menu_item, 'count': item_count, 'additional_info': additional_item_info})
            order_sum = order_sum + item_price

        order_sum = round(order_sum, 2)

    return order_items, order_sum
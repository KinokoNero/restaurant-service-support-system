from flask import Blueprint, request, redirect, url_for, session

from authentication import login_required, role_required, current_user
from classes import Role, OrderItem, Order, ServiceRequestType, ServiceRequest
from database import get_menu_item, insert_order, insert_service_request

session_routes = Blueprint('session_routes', __name__, template_folder='templates')


# Order
@session_routes.route('/add-to-order/<item_id>', methods=['POST'])
@login_required
@role_required(Role.USER)
def add_to_order(item_id):
    if 'order' not in session:
        session['order'] = []

    menu_item = get_menu_item(item_id)
    order_item = OrderItem(menu_item=menu_item, count=1, additional_info='')
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

        order_item.count = request.form.get('item-count', order_item.count)
        order_item.additional_info = request.form.get('additional-info', order_item.additional_info)

        order_item_dict = order_item.to_dict()
        session['order'][item_index] = order_item_dict

    return redirect(url_for('current_user_order'))


def get_current_user_order_info():
    if 'order' not in session:
        session['order'] = []

    order_items = []
    price_sum = 0

    for order_item_dict in session['order']:
        order_item = OrderItem.from_dict(order_item_dict)
        order_items.append(order_item)

        price_sum = price_sum + order_item.menu_item.price * order_item.count
        price_sum = round(price_sum, 2)

    return order_items, price_sum


@session_routes.route('/place-order', methods=['POST'])
@login_required
@role_required(Role.USER)
def place_order():  # TODO: collapse multiple separate identical menu items into a single one with approporiate count value
    if 'order' in session:
        order_list = session['order']
        order_items = []
        for order_item_dict in order_list:
            order_items.append(OrderItem.from_dict(order_item_dict))

        order = Order(orderer=current_user, order_items=order_items)

        result_successful = insert_order(order)
        if result_successful:
            session['order'] = []

    return redirect(url_for('menu'))


# User requests
@session_routes.route('/submit-service-request', methods=['POST'])
@login_required
@role_required(Role.USER)
def submit_service_request():
    request_type = ServiceRequestType(request.form['request-type'])
    service_request = ServiceRequest(requester=current_user, request_type=request_type)

    if request_type == ServiceRequestType.CUSTOM:
        service_request.custom_info = request.form['custom-info']

    insert_service_request(service_request)

    return redirect(url_for('menu'))

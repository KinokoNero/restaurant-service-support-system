from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_session import Session
from bson import ObjectId
from database import menu_collection

session_routes = Blueprint('session_routes', __name__, template_folder='templates')

class OrderItem:
    def __init__(self, menu_item, additional_info=""):
        self.menu_item = menu_item
        self.additional_info = additional_info

@session_routes.route('/add-to-order/<item_id>')
def add_to_order(item_id):
    item = menu_collection.find_one({'_id': ObjectId(item_id)})
    additional_info = request.form['additional-info']

    # Initialize order for session
    if 'order' not in session:
        session['order'] = []

    order_item = OrderItem(item, additional_info)
    
    session['order'].append(order_item)

    #TODO: redirect to different pages based on where the request was sent from (from main page or from order manager)
    return redirect(url_for('menu'))
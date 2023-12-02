from enum import Enum
from bson import ObjectId
from flask_login import UserMixin
from datetime import datetime

class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(UserMixin):
    def __init__(self, name, role, id=None, qr_code_image_id=None):
        self.name = name
        if not isinstance(role, Role):
            raise ValueError("Argument 'role' of object User must be an instance of Role enum.")
        self.role = role
        self.id = ObjectId(id)
        self.qr_code_image_id = ObjectId(qr_code_image_id)

    def to_dict(self):
        user = {
            'name': self.name,
            'role': self.role.value
        }
        if self.qr_code_image_id is not None:
            user['_id'] = ObjectId(self.id)
        if self.qr_code_image_id is not None:
            user['qr_code_image_id'] = ObjectId(self.qr_code_image_id)

        return user

    @classmethod
    def from_dict(cls, user_dict):
        return cls(
            name=user_dict['name'],
            role=Role(user_dict['role']),
            id=ObjectId(user_dict.get('_id')),
            qr_code_image_id=ObjectId(user_dict.get('qr_code_image_id'))
        )

class MenuItem: # Represents a single menu item stored in database
    def __init__(self, name, description, price, image_id, id=None):
        self.name = name
        self.description = description
        self.price = price
        self.image_id = image_id
        self.id = ObjectId(id)

    def to_dict(self):
        menu_item = {
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'image_id': ObjectId(self.image_id),
        }
        if self.id is not None:
            menu_item['_id'] = ObjectId(self.id)

        return menu_item

    @classmethod
    def from_dict(cls, menu_item_dict):
        return cls(
            name=menu_item_dict['name'],
            description=menu_item_dict['description'],
            price=float(menu_item_dict['price']),
            image_id=menu_item_dict['image_id'],
            id=ObjectId(menu_item_dict.get('_id'))
        )

class OrderItem: # Represents a single order item stored in session
    def __init__(self, menu_item, count, additional_info):
        if not isinstance(menu_item, MenuItem):
            raise ValueError("Argument 'menu_item' of object OrderItem must be an instance of class MenuItem.")
        self.menu_item = menu_item

        self.count = count
        self.additional_info = additional_info

    def to_dict(self):
        return {
            'menu_item': self.menu_item.to_dict(),
            'count': int(self.count),
            'additional_info': self.additional_info,
        }

    @classmethod
    def from_dict(cls, order_item_dict):
        return cls(
            menu_item=MenuItem.from_dict(order_item_dict['menu_item']),
            count=int(order_item_dict['count']),
            additional_info=order_item_dict['additional_info'],
        )

class OrderStatus(Enum):
    NEW = 'new',
    FINISHED = 'finished'

class Order: # Represents the whole order for storage in database
    def __init__(self, orderer, order_items, status, id=None):
        if not isinstance(orderer, User):
            raise ValueError("Argument 'orderer' of object Order must be an instance of class User.")
        self.orderer = orderer

        if not isinstance(order_items, list) or not all(isinstance(item, OrderItem) for item in order_items):
            raise ValueError("Argument 'order_items' of object Order must be a dictionary of OrderItem objects.")
        self.order_items = order_items

        self.timestamp = datetime.timestamp(datetime.now())

        if not isinstance(status, OrderStatus):
            raise ValueError("Argument 'status' of object Order must be an instance of OrderStatus enum.")
        self.status = status

        self.id = ObjectId(id)

    def to_dict(self):
        order_items_dict = []
        for order_item in self.order_items:
            order_items_dict.append(order_item.to_dict())

        order_dict = {
            'orderer': self.orderer.to_dict(),
            'order_items': order_items_dict,
            'timestamp': self.timestamp,
            'status': self.status.value
        }
        if self.id is not None:
            order_dict['_id'] = ObjectId(self.id)

        return order_dict

    @classmethod
    def from_dict(cls, order_dict):
        order_items_dict = order_dict['order_items']
        order_items = []
        for order_item_dict in order_items_dict:
            order_item = OrderItem.from_dict(order_item_dict)
            order_items.append(order_item)

        return cls(
            orderer=User.from_dict(order_dict['orderer']),
            order_items=order_items,
            timestamp=order_dict['timestamp'],
            status=order_dict['status'],
            id=ObjectId(order_dict.get('_id'))
        )
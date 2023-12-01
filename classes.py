from enum import Enum
from flask_login import UserMixin

class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(UserMixin):
    def __init__(self, id, name, role, qr_code_image_id=None):
        self.id = id
        self.name = name
        if not isinstance(role, Role):
            raise ValueError("Argument 'role' of object User must be an instance of Role enum.")
        self.role = role
        self.qr_code_image_id = qr_code_image_id

    def to_dict(self):
        user = {
            'id': self.id,
            'name': self.name,
            'role': self.role.value,
            'qr_code_image_id': str(self.qr_code_image_id)
        }
        #if self._id is not None:
         #   menu_item['id'] = str(self.id)
        if self.qr_code_image_id is not None:
            menu_item['qr_code_image_id'] = str(self.qr_code_image_id)

        return user

    @classmethod
    def from_dict(cls, user_dict):
        return cls(
            id=user_dict['_id'],
            name=user_dict['name'],
            role=Role(user_dict['role']),
            #_id=user_dict.get('_id'),
            qr_code_image_id=user_dict.get('qr_code_image_id')
        )

class MenuItem: # Represents a single menu item stored in database
    def __init__(self, name, description, price, image_id, _id=None):
        self.name = name
        self.description = description
        self.price = price
        self.image_id = image_id
        self._id = _id

    def to_dict(self):
        menu_item = {
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'image_id': str(self.image_id),
        }
        if self._id is not None:
            menu_item['_id'] = str(self._id)

        return menu_item

    @classmethod
    def from_dict(cls, menu_item_dict):
        return cls(
            name=menu_item_dict['name'],
            description=menu_item_dict['description'],
            price=float(menu_item_dict['price']),
            image_id=menu_item_dict['image_id'],
            _id=menu_item_dict.get('_id')
        )

class OrderItem: # Represents a single order item stored in session
    def __init__(self, menu_item, count, additional_info):
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

"""class Order: # Represents the whole order for storage in database
    def __init__(order_items):
        self.order_items = order_items

    def to_dict(self):
        order_items_dict = []
        for order_item in self.order_items:
            order_items_dict.append(order_item.to_dict())

        return {
            'order_items': self.order_items.to_dict()
        }

    @classmethod
    def from_dict(cls, order_item_dict):
        return cls(
            
        )"""
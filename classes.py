from enum import Enum
from bson import ObjectId
from flask_login import UserMixin
from datetime import datetime


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'


class User(UserMixin):
    def __init__(self, name, role, id=None, qr_code_image_id=None, password=None, salt=None):
        self.name = name
        if not isinstance(role, Role):
            raise ValueError("Argument 'role' of object User must be an instance of Role enum.")
        self.role = role
        self.id = id
        self.qr_code_image_id = qr_code_image_id
        self.password = password
        self.salt = salt

    def to_dict(self):
        user = {
            'name': self.name,
            'role': self.role.value
        }
        if self.id is not None:
            user['_id'] = ObjectId(self.id)
        if self.qr_code_image_id is not None:
            user['qr_code_image_id'] = ObjectId(self.qr_code_image_id)
        if self.password is not None:
            user['password'] = self.password
        if self.salt is not None:
            user['salt'] = self.salt

        return user

    @classmethod
    def from_dict(cls, user_dict):
        return cls(
            name=user_dict['name'],
            role=Role(user_dict['role']),
            id=user_dict.get('_id'),
            qr_code_image_id=user_dict.get('qr_code_image_id'),
            password=user_dict.get('password'),
            salt=user_dict.get('salt')
        )


class MenuItem:  # Represents a single menu item stored in database
    def __init__(self, name, price, id=None, description=None, image_id=None):
        self.name = name
        self.price = price
        self.id = id
        self.description = description
        self.image_id = image_id

    def to_dict(self):
        menu_item = {
            'name': self.name,
            'description': self.description,
            'price': float(self.price)
        }
        if self.id is not None:
            menu_item['_id'] = ObjectId(self.id)
        if self.description is not None:
            menu_item['description'] = self.description
        if self.image_id is not None:
            menu_item['image_id'] = ObjectId(self.image_id)

        return menu_item

    @classmethod
    def from_dict(cls, menu_item_dict):
        return cls(
            name=menu_item_dict['name'],
            price=float(menu_item_dict['price']),
            id=menu_item_dict.get('_id'),
            description=menu_item_dict.get('description'),
            image_id=menu_item_dict.get('image_id')
        )


class OrderItem:  # Represents a single order item stored in session
    def __init__(self, menu_item, count, additional_info):
        if not isinstance(menu_item, MenuItem):
            raise ValueError("Argument 'menu_item' of OrderItem class object must be an instance of MenuItem class.")
        self.menu_item = menu_item
        self.count = count
        self.additional_info = additional_info

    def to_dict(self):
        return {
            'menu_item': self.menu_item.to_dict(),
            'count': int(self.count),
            'additional_info': str(self.additional_info)
        }

    @classmethod
    def from_dict(cls, order_item_dict):
        return cls(
            menu_item=MenuItem.from_dict(order_item_dict['menu_item']),
            count=int(order_item_dict['count']),
            additional_info=str(order_item_dict['additional_info']),
        )


class Status(Enum):
    NEW = 'new'
    FINISHED = 'finished'


status_display_strings = {
    Status.NEW: 'Nowe',
    Status.FINISHED: 'Zakończone'
}


class Order:  # Represents the whole order for storage in database
    def __init__(self, orderer, order_items, id=None, status=Status.NEW, price_sum=0, timestamp=datetime.timestamp(datetime.now())):
        if not isinstance(orderer, User):
            raise ValueError("Argument 'orderer' of Order class object must be an instance of User class.")
        self.orderer = orderer

        if not isinstance(order_items, list) or not all(isinstance(item, OrderItem) for item in order_items):
            raise ValueError("Argument 'order_items' of Order class object must be a dictionary of OrderItem objects.")
        self.order_items = order_items

        self.id = id

        if not isinstance(status, Status):
            raise ValueError("Argument 'status' of Order class object must be an instance of Status enum.")
        self.status = status

        self.price_sum = float(price_sum)
        self.timestamp = timestamp

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
            status=Status(order_dict['status']),
            id=order_dict.get('_id')
        )


class ServiceRequestType(Enum):
    CHECK = 'check'
    HELP = 'help'
    CUSTOM = 'custom'


service_request_type_display_strings = {
    ServiceRequestType.CHECK: 'Prośba o rachunek',
    ServiceRequestType.HELP: 'Prośba o pomoc',
    ServiceRequestType.CUSTOM: 'Prośba niestandardowa'
}


class ServiceRequest:
    def __init__(self, requester, request_type, id=None, status=Status.NEW, custom_info=None):
        if not isinstance(requester, User):
            raise ValueError("Argument 'requester' of UserRequest class object must be an instance of User class.")
        self.requester = requester

        if not isinstance(request_type, ServiceRequestType):
            raise ValueError("Argument 'request_type' of UserRequest class object must be an instance of ServiceRequestType enum.")
        self.request_type = request_type

        self.id = id

        if not isinstance(status, Status):
            raise ValueError("Argument 'status' of object UserRequest must be an instance of Status enum.")
        self.status = status

        self.custom_info = custom_info
        self.timestamp = datetime.timestamp(datetime.now())

    def to_dict(self):
        service_request_dict = {
            'requester': self.requester.to_dict(),
            'request_type': self.request_type.value,
            'status': self.status.value,
            'timestamp': self.timestamp
        }
        if self.id is not None:
            service_request_dict['_id'] = ObjectId(self.id)
        if self.custom_info is not None:
            service_request_dict['custom_info'] = self.custom_info

        return service_request_dict

    @classmethod
    def from_dict(cls, service_request_dict):
        return cls(
            requester=User.from_dict(service_request_dict['requester']),
            request_type=ServiceRequestType(service_request_dict['request_type']),
            custom_info=service_request_dict.get('custom_info'),
            status=Status(service_request_dict['status']),
            id=service_request_dict.get('_id')
        )

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


class MenuItem:  # Represents a single menu item stored in database
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


class OrderItem:  # Represents a single order item stored in session
    def __init__(self, menu_item_id, count, additional_info, menu_item=None):
        self.menu_item_id = ObjectId(menu_item_id)
        self.count = count
        self.additional_info = additional_info

    def to_dict(self):
        return {
            'menu_item_id': ObjectId(self.menu_item_id),
            'count': int(self.count),
            'additional_info': str(self.additional_info)
        }

    @classmethod
    def from_dict(cls, order_item_dict):
        return cls(
            menu_item_id=ObjectId(order_item_dict['menu_item_id']),
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
    def __init__(self, orderer_id, order_items, id=None, status=Status.NEW, orderer=None, price_sum=0, timestamp=None):
        self.orderer_id = ObjectId(orderer_id)

        if not isinstance(order_items, list) or not all(isinstance(item, OrderItem) for item in order_items):
            raise ValueError("Argument 'order_items' of object Order must be a dictionary of OrderItem objects.")
        self.order_items = order_items

        self.id = ObjectId(id)

        if not isinstance(status, Status):
            raise ValueError("Argument 'status' of object Order must be an instance of Status enum.")
        self.status = status

        self.orderer = orderer
        self.price_sum = float(price_sum)
        self.timestamp = datetime.timestamp(datetime.now())

    def to_dict(self):
        order_items_dict = []
        for order_item in self.order_items:
            order_items_dict.append(order_item.to_dict())

        order_dict = {
            'orderer_id': ObjectId(self.orderer_id),
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
            orderer_id=order_dict['orderer_id'],
            order_items=order_items,
            timestamp=order_dict['timestamp'],
            status=Status(order_dict['status']),
            id=ObjectId(order_dict.get('_id'))
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
    def __init__(self, requester_id, request_type, custom_info=None, status=Status.NEW):
        self.requester_id = ObjectId(requester_id)

        if not isinstance(request_type, ServiceRequestType):
            raise ValueError("Argument 'request_type' of object UserRequest must be an instance of RequestType enum.")
        self.request_type = request_type

        if not isinstance(status, Status):
            raise ValueError("Argument 'status' of object UserRequest must be an instance of Status enum.")
        self.status = status

        self.custom_info = custom_info
        self.timestamp = datetime.timestamp(datetime.now())

    def to_dict(self):
        user_request_dict = {
            # 'requester': self.requester.to_dict(),
            'requester_id': ObjectId(self.requester_id),
            'request_type': self.request_type.value,
            'status': self.status.value,
            'timestamp': self.timestamp
        }
        if self.custom_info is not None:
            user_request_dict['custom_info'] = self.custom_info

        return user_request_dict

    @classmethod
    def from_dict(cls, user_request_dict):
        return cls(
            requester_id=ObjectId(user_request_dict['requester_id']),
            request_type=user_request_dict['request_type'],
            custom_info=user_request_dict.get('custom_info'),
            status=Status(user_request_dict['status'])
        )

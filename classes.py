class MenuItem:
    def __init__(self, name, description, price, image_id, _id=None):
        self.name = name
        self.description = description
        self.price = price
        self._id = _id
        self.image_id = image_id

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

class OrderItem:
    def __init__(self, menu_item, count, additional_info):
        #self.menu_item_id = menu_item_id
        self.menu_item = menu_item
        self.count = count
        self.additional_info = additional_info

    def to_dict(self):
        return {
            #'menu_item_id': ObjectId(self.menu_item_id),
            'menu_item': self.menu_item.to_dict(),
            'count': int(self.count),
            'additional_info': self.additional_info,
        }
        #return order_item

    @classmethod
    def from_dict(cls, order_item_dict):
        return cls(
            menu_item = MenuItem.from_dict(order_item_dict['menu_item']), #ObjectId(order_item_dict['menu_item_id']),
            count = int(order_item_dict['count']),
            additional_info = order_item_dict['additional_info'],
        )
class User:
    def __init__(self, name, email, password):
        self.name=name
        self.email=email
        self.password=password


class Sellers:
    def __init__(self, name, email, password):
        self.name=name
        self.email=email
        self.password=password

class Product:
    def __init__(self, name, description, brand, category, price,seller_id, color, size):
        self.name = name
        self.description = description
        self.brand = brand
        self.category = category
        self.price = price
        self.seller_id = seller_id
        self.color=color
        self.size=size

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "brand": self.brand,
            "category": self.category,
            "price": self.price,
            "seller_id": self.seller_id,
            "size": self.size,
            "color": self.color
        }


        
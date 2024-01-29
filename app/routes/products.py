from app import app, request,jsonify, mongo
from app.models import Product
from app.functions import get_role
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@app.route('/get_products', methods=['GET'])
def get_products():
    total_products=[]
    products=mongo.db.products.find()
    for product in products:
        pro={
            "product_id":product["product_id"],
            "name":product['name'],
            "description":product['description'],
            "brand":product['brand'],
            "category":product['category'],
            "price":product['price'],
            "seller_id":product['seller_id'],
            "color":product['color'],
            "size":product['size']
        }
        total_products.append(pro)
    return jsonify(total_products)


@app.route('/add_products', methods=['POST'])
@jwt_required()
def add_products():
    identity= get_jwt_identity()
    role= get_role(identity=identity)
    if role=="Seller":
        name= request.json['name']
        description= request.json['description']
        brand= request.json['brand']
        category= request.json['category']
        price=request.json['price']
        seller_id= request.json['seller_id']
        color= request.json['color']
        size=request.json['size']
        product_id=request.json['product_id']
        product= Product(name=name, description=description, brand=brand, category=category,price=price, seller_id=seller_id, size=size, color=color, product_id=product_id)
        product_data= product.to_dict()
        mongo.db.products.insert_one(product_data)
        return jsonify({"success":"Product added"}),200
    else:
        return jsonify({"Error":"You are not authorized to access this route"})


@app.route('/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user=get_jwt_identity()
    product_id= request.json['product_id']
    quantity=request.json['quantity']
    user_collection= f"{user}_cart"
    product= mongo.db.products.find_one({"product_id":product_id})
    if product and quantity:
        mongo.db[user_collection].insert_one({"user":user, "product_id":product_id, "quantity":quantity})
        return jsonify({"Success": "Item added to cart"})
    else:
        return jsonify({"Error":"Give product id and quantity"})


@app.route('/get_cart_products', methods=['GET'])
@jwt_required()
def get_cart_products():
    cart=[]
    user= get_jwt_identity()
    collection=f"{user}_cart"
    cart_items=mongo.db[collection].find()
    for item in cart_items:
        product_id= item['product_id']
        product= mongo.db.products.find_one({"product_id":product_id})
        if product:
            cartItems={
                'name':product['name'],
                'description':product['description'],
                'brand':product['brand'],
                'category':product['category'],
                'price':product['price'],
                'seller_id':product['seller_id'],
                'color':product['color'],
                'size':product['size'],
                'product_id':product['product_id']
            }
        else:
            return jsonify({"Error":"Product not available"})
        cart.append(cartItems)
    return jsonify(cart)

@app.route('/remove_from_cart', methods=['DELETE'])
@jwt_required()
def remove_from_cart():
    product_id=request.json['product_id']
    identity= get_jwt_identity()
    collection =f"{identity}_cart"
    product= mongo.db[collection].find_one({"product_id":product_id})
    if product:
        mongo.db[collection].delete_one({"product_id":product_id})
        return jsonify({"Success": "Product successfully removed from cart"}), 200
    else:
        return jsonify({"Error":"Product not found"}),401
    
@app.route('/clear_cart', methods=['DELETE'])
@jwt_required()
def clear_cart():
    identity= get_jwt_identity()
    collection= f'{identity}_cart'
    mongo.db[collection].drop()
    return jsonify({"Success":"All items removed from cart"})


@app.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    identity=get_jwt_identity()
    role= get_role(identity=identity)
    claim=get_jwt()
    return jsonify({
        "identity":identity,
        "claim":claim,
        "role":role
    })
    

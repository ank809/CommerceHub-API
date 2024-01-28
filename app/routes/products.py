from app import app, request,jsonify, mongo
from app.models import Product
from app.functions import get_role
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@app.route('/get_products')
def get_products():
    pass


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
        product= Product(name=name, description=description, brand=brand, category=category,price=price, seller_id=seller_id, size=size, color=color)
        product_data= product.to_dict()
        mongo.db.products.insert_one(product_data)
        return jsonify({"success":"Product added"}),200
    else:
        return jsonify({"Error":"You are not authorized to access this route"})



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
    

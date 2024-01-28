from app import app, request, mongo, jsonify
from app.functions import isValidEmail, isValidPassword
from app.models import User, Sellers

@app.route('/')
def hello():
    return 'HELLO WORLD!'

@app.route('/register_user', methods=['POST'])
def register_user():
    name=request.json['name']
    email=request.json['email']
    password= request.json['password']

    if mongo.db.users.find_one({"name":name ,"email":email}):
        return jsonify({"error":"this user already exists"})
    
    if not isValidEmail(email=email):
        return jsonify({"error":"Please enter a valid email"})
    
    if not isValidPassword(password=password):
        return jsonify({"error":"Please enter a password that contains uppercase, lowercase , digits and special characters"})
    
    user= User(name=name, email=email,password=password)
    mongo.db.users.insert_one({
        'name':user.name,
        'email':user.email,
        'password':user.password
    })
    return jsonify({'success':"Account Successfully created"}),200

@app.route('/register_seller', methods=['POST'])
def register_seller():
    name=request.json['name']
    email=request.json['email']
    password= request.json['password']

    
    if not isValidEmail(email=email):
        return jsonify({"error":"Please enter a valid email"})
    
    if not isValidPassword(password=password):
        return jsonify({"error":"Please enter a password that contains uppercase, lowercase , digits and special characters"})
    
    if mongo.db.sellers.find_one({"name":name ,"email":email}):
        return jsonify({"error":"this seller account already exists"})
    
    seller= Sellers(name=name, email=email,password=password)
    mongo.db.sellers.insert_one({
        'name':seller.name,
        'email':seller.email,
        'password':seller.password
    })
    return jsonify({'success':"Account Successfully created"}),200
from app import app, request, mongo, jsonify
from app.functions import isValidEmail, isValidPassword
from app.models import User, Sellers
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

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


@app.route('/login_user', methods=['POST'])
def user_login():
    name= request.json['name']
    password=request.json['password']
    user=mongo.db.users.find_one({"name":name})
    if user and user['password']==password:
        access_token= create_access_token(identity=name)
        refresh_token= create_refresh_token(identity=name)
        return jsonify({
            "success":"Successfully logged in",
            "name":name,
            "access_token":access_token,
            "refresh_token":refresh_token
        }),200
    else:
        return jsonify({"Error":"Invalid credentials"}),401
    

@app.route('/login_seller', methods=['POST'])
def seller_login():
    name= request.json['name']
    password=request.json['password']
    seller=mongo.db.sellers.find_one({"name":name})
    if seller and seller['password']==password:
        access_token= create_access_token(identity=name)
        refresh_token= create_refresh_token(identity=name)
        return jsonify({
            "success":"Successfully logged in",
            "name":name,
            "access_token":access_token,
            "refresh_token":refresh_token
        }),200
    else:
        return jsonify({"Error":"Invalid credentials"}),401
    
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    identity=get_jwt()
    jti= identity['jti']
    mongo.db.revoked_tokens.insert_one({"jti":jti})
    return jsonify({"Success": "Logout Successfully"})

@app.route("/refresh_token", methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity= get_jwt_identity()
    access_token= create_access_token(identity=identity)
    return jsonify({"Success":"New token allocated", "Access_token":access_token, "Identity":identity}),200

from flask import Flask, request, jsonify
from config import SECRET_KEY, Mongo_URI, JWT_SECRET_KEY
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from datetime import timedelta
app=  Flask(__name__)

app.config['SECRET_KEY']=SECRET_KEY
app.config['MONGO_URI']=Mongo_URI
app.config['JWT_SECRET_KEY']=JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(minutes=20)

mongo= PyMongo(app)
jwt= JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"error":"Token has been expired"}),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error":"Token is invalid"}),401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"error":"Unauthorized access"})

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti= jwt_data['jti']
    return mongo.db.revoked_tokens.find_one({"jti":jti})

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return {
        "msg":"user has been logged out",
        "error":"token has been revoked"
    }

from app.routes import auth, products
from flask import Flask, request, jsonify
from config import SECRET_KEY, Mongo_URI
from flask_pymongo import PyMongo

app=  Flask(__name__)

app.config['SECRET_KEY']=SECRET_KEY
app.config['MONGO_URI']=Mongo_URI

mongo= PyMongo(app)

from app.routes import auth
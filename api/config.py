import os

from .routes import api_routes

from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import request, jsonify
import redis
from dotenv import load_dotenv

load_dotenv()
class Config:

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

    SECRET_KEY = os.getenv('SECRET_KEY')

def valid_login(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):

        current_user = get_jwt_identity()

        if 'logged-in' not in current_user:
            return jsonify({'error': 'No ha iniciado sesión'}), 401
        
        return func(*args, **kwargs)

    return wrapper

def valid_role(route:str):
    def decorator(func:callable):
        @wraps(func)
        @jwt_required()
        def wrapper(*args,**kwargs):

            current_user = get_jwt_identity()

            if 'role' not in current_user:
                return jsonify({'error': 'No tienes un rol'}), 401

            role = current_user.get('role')
            routes_by_role = api_routes[role]
            
            if route not in routes_by_role:
                return jsonify({'error':'esta ruta no esta disponible para tu rol'}),403

            return func(*args, **kwargs)
        return wrapper
    return decorator
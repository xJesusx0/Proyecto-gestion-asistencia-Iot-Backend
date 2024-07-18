from functools import wraps
from flask import request, jsonify,session
from .routes import api_routes
from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_DB = os.getenv('MYSQL_DB')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

SECRET_TOKEN = '1234'

def valid_token(token):
    return token == SECRET_TOKEN

def token_required (func:callable):
    @wraps(func)
    def wrapper(*args,**kwargs):

        token = request.headers.get('token')

        if not token or not valid_token(token):
            return jsonify({'message': 'Invalid token'}), 401

        return func(*args, **kwargs)
    
    return wrapper

def valid_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'logged-in' not in session or not session['logged-in']:
            return jsonify({'error': 'No ha iniciado sesión'}), 401
        
        return func(*args, **kwargs)

    return wrapper



def valid_role(route:str):
    def decorator(func:callable):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if 'role' not in session or not session['role']:
                return jsonify({'error': 'No tienes un rol'}), 401

            role = session.get('role')
            routes_by_role = api_routes[role]
            
            if route not in routes_by_role:
                return jsonify({'error':'esta ruta no esta disponible para tu rol'}),403

            return func(*args, **kwargs)
        return wrapper
    return decorator
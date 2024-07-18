from functools import wraps
from flask import request, jsonify,session
from .routes import api_routes

class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'contraseña'
    MYSQL_DB = 'proyecto'
    SECRET_KEY = 'secret'
    IP = '127.0.0.1' # Tu ip

SECRET_TOKEN = 'token'

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

def valid_login(func:callable):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session:
            return jsonify({'error': 'No ha iniciado sesion'}), 401
        
        if not session['logged-in']:
            return jsonify({'error': 'No ha iniciado sesion'}), 401
        
        return func(*args, **kwargs)

    return wrapper

def valid_role(route:str):
    def decorator(func:callable):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if 'role' not in session or not session['role']:
                return jsonify({'error': 'No ha iniciado sesion'}), 401

            role = session.get('role')
            routes_by_role = api_routes[role]
            
            if route not in routes_by_role:
                return jsonify({'error':'esta ruta no esta disponible para tu rol'}),403

            return func(*args, **kwargs)
        return wrapper
    return decorator
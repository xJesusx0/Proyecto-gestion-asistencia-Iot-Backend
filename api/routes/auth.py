from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from . import web_routes
from Database.auth import *
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    request_body = request.get_json()

    response = validateLogin(request_body)

    if response is None:
        return jsonify({'error': 'Datos incorrectos'}), 401

    roles = get_roles(response['id_usuario'])
    
    identity = {
        'user-id' : response['id_usuario'],
        'logged-in' : True
    }

    if len(roles) == 1:
        identity['role'] = roles[0]['nombre'].lower()

    expires = timedelta(minutes=30)
    access_token = create_access_token(identity = identity,expires_delta=expires)

    data_to_send = {
        'id_usuario':response.get('id_usuario'),
        'correo':response.get('correo'),
        'nombres':response.get('nombres'),
        'apellidos':response.get('apellidos')
    }

    data = {
        'user-data': data_to_send,
        'roles': roles,
        'access_token': access_token
    }

    print(data)
    print(identity)
    return jsonify(data), 200

@auth_bp.route('/set-role', methods=['POST'])
@jwt_required()
def set_role():
    request_body = request.get_json()
    
    current_user = get_jwt_identity()

    if 'role' in current_user:
        return jsonify({'error':'Ya tienes un rol'})

    if 'role' in request_body:
        current_user['role'] = request_body['role'].lower()
        expires = timedelta(minutes=30)
        access_token = create_access_token(identity=current_user,expires_delta=expires)
        return jsonify({'response': 'Operación exitosa','access_token':access_token}), 200
    
    return jsonify({'error': 'Se esperaba un rol'}), 400

@auth_bp.route('/validate-login', methods=['GET'])
@jwt_required()
def validate_login():
    try:     
        current_user = get_jwt_identity()
        logged_in = current_user.get('logged-in', False)
        return jsonify({'response': logged_in})
    except Exception as e:
        return jsonify({'error':'Web token invalido'}),422

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    current_user['logged-in'] = False
    return jsonify({'response': 'Sesión limpiada correctamente'}), 200

@auth_bp.route('/validate-role', methods=['GET'])
@jwt_required()
def validate_role():    

    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'Se esperaba un parámetro "url" en la solicitud'}), 400
    
    current_user = get_jwt_identity()
    role = current_user.get('role')

    if not role or role not in web_routes:
        return jsonify({'valid-role': False, 'valid-route': False}), 401

    valid_route = url in web_routes[role]
    valid_role = True  

    return jsonify({'valid-role': valid_role, 'valid-route': valid_route})

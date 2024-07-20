from flask import Blueprint, request, jsonify, session

from . import web_routes

from api.config import token_required

from Database.auth import *

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    request_body = request.get_json()

    response = validateLogin(request_body)

    if response is None:
        return jsonify({'error': 'Datos incorrectos'}), 401

    roles = get_roles(response['id_usuario'])
    
    
    session['logged-in'] = True
    session['user-id'] = response['id_usuario']
    if len(roles) == 1:
        session['role'] = roles[0]['nombre'].lower()

    data_to_send = {
        'id_usuario':response.get('id_usuario'),
        'correo':response.get('correo'),
        'nombres':response.get('nombres'),
        'apellidos':response.get('apellidos')
    }

    data = {
        'user-data': data_to_send,
        'roles': roles
    }

    print(data)
    print(session)
    return jsonify(data), 200

@auth_bp.route('/set-role', methods=['POST'])
@token_required
def set_role():
    request_body = request.get_json()

    if 'role' in session:
        return jsonify({'error':'Ya tienes un rol'})

    if 'role' in request_body:
        session['role'] = request_body['role'].lower()
        return jsonify({'response': 'Operación exitosa'}), 200
    
    return jsonify({'error': 'Se esperaba un rol'}), 400

@auth_bp.route('/validate-login', methods=['GET'])
@token_required
def validate_login():
    print(session)
    logged_in = session.get('logged-in', False)
    return jsonify({'response': logged_in})

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    session.clear()  
    print(session)
    return jsonify({'response': 'Sesión limpiada correctamente'}), 200

@auth_bp.route('/validate-role', methods=['GET'])
@token_required
def validate_role():    

    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'Se esperaba un parámetro "url" en la solicitud'}), 400

    role = session.get('role')

    if not role or role not in web_routes:
        return jsonify({'valid-role': False, 'valid-route': False}), 401

    valid_route = url in web_routes[role]
    valid_role = True  

    return jsonify({'valid-role': valid_role, 'valid-route': valid_route})

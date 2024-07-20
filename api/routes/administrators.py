import io
import csv
import json
import re
from datetime import datetime

from flask import Blueprint, request, jsonify, session

from ..config import *

from Database import valid_table, encode_time
from Database.encrypt import encrypt
from Database.auth import get_roles
from Database.administrators import *
from Database.students import get_groups_by_students_id
from Database.teachers import get_groups_by_teachers_id, get_all_teachers
from Database.groups import group_exists, insert_group, is_time_overlap

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')

def format_time(time_str:str):
    return datetime.strptime(time_str, '%H:%M').strftime('%H:%M:%S')

def validate_email(email):
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_pattern, email) is not None

def validate_phone(phone):
    phone_pattern = r'^\d{10}$'
    return re.match(phone_pattern, phone) is not None

def valid_csv(stream,table:set):
    stream.seek(0)

    csv_to_dict = csv.DictReader(stream)

    first_row = next(csv_to_dict, None)
    if first_row is None:
        return False  

    valid_list = all(table.issubset(element.keys()) for element in csv_to_dict)
    return valid_list

@admin_bp.route('/get-users')
@token_required
@valid_login
@valid_role('get-users')
def get_users():
    print(session)
    users = get_all_users()
    if not users:
        return jsonify({'error':'Ha ocurrido un error'})
    return jsonify(users),200

@admin_bp.route('/get-user-data')
@token_required
@valid_login
@valid_role('get-user-data')
def get_user_info():
    try:
        user_id = request.args.get('id')

        if not user_id:
            return jsonify({'error': 'No se proporcionó un id de usuario'}), 400

        user_info = get_user( user_id)
        user_roles = get_roles( user_id)

        if not user_info or not user_roles:
            return jsonify({'error': 'Ha ocurrido un error al obtener la información'}), 404

        roles = [role['id_rol'] for role in user_roles]
        groups = []

        if 3 in roles:
            groups = get_groups_by_students_id( user_id)
        elif 2 in roles:
            groups = get_groups_by_teachers_id( user_id)

        groups_json = encode_time(groups)

        return jsonify({
            'user_info': user_info,
            'user_roles': user_roles,
            'groups': groups_json
        }), 200

    except Exception as e:
        return jsonify({'error': f'Ha ocurrido un error: {str(e)}'}), 500


@admin_bp.route('/get-modules')
@token_required
@valid_login
@valid_role('get-modules')
def get_modules():
    modules = get_all_modules()
    return jsonify(modules)

@admin_bp.route('/get-teachers')
@token_required
@valid_login
@valid_role('get-teachers')
def get_teachers():
    teachers = get_all_teachers()
    return jsonify(teachers),200

@admin_bp.route('/get-classrooms')
@token_required
@valid_login
@valid_role('get-classrooms')
def get_classrooms():
    classrooms = get_all_classrooms()
    return jsonify(classrooms),200
 

@admin_bp.route('add-group',methods = ['POST'])
@token_required
@valid_login
@valid_role('add-group')
def add_group():

    request_body = request.get_json()
    
    if not request_body:
        return jsonify({'error':'se esperaba un grupo'}),400

    expected_keys = ['group-id', 'module', 'teacher', 'classroom', 'period', 'weekday', 'start-time', 'end-time']

    for key in expected_keys:
        if key not in request_body or not request_body[key]:
            return jsonify({'error':f'Json invalido, se esperaba el campo {key}'}),400

    try:
        request_body['classroom'] = int(request_body.get('classroom'))
    except:
        return jsonify({'error':'Id de salon invalida'}),400

    request_body['group-id'] = request_body.get('group-id', '').upper()
    request_body['start-time'] = format_time(request_body['start-time'])
    request_body['end-time'] = format_time(request_body['end-time'])

    request_to_list = []

    for key in expected_keys:
        request_to_list.append(request_body.get(key))

    request_to_tuple = tuple(request_to_list)

    group = group_exists(request_body)
    
    if group != None:
        group_json = encode_time(group)
        return jsonify({'error':'El grupo ya existe','info' : group_json }),409

    overlap = is_time_overlap(request_body['classroom'],request_body['weekday'],request_body['start-time'],request_body['end-time'])
    
    if overlap != None:
        overlap_json = encode_time(overlap)
        return(jsonify({'error':'Cruce de horarios','info':overlap_json})),409

    res =  insert_group(request_to_tuple)

    if res == 'ok':
        return jsonify({'response':'Operacion realizada correctamente'}),200
    
    return jsonify({'error':f'Ha ocurrido un error: {res}'}),500

@admin_bp.route('/upload-and-register-users', methods=['POST'])
@token_required
@valid_login
@valid_role('upload-and-register-users')
def upload_and_register_users():
    if 'csvFile' not in request.files:
        return jsonify({'response': 'Se esperaba un archivo'}), 400

    file = request.files['csvFile']

    if file.filename == '':
        return jsonify({'response': 'No se selecciono un archivo'}), 400

    table = request.form.get('table')
    if not table:
        return jsonify({'response': 'Se esperaba una tabla'}), 400

    columns = valid_table(table)

    if columns == None:
        print('1232')
        return jsonify({'response':'Columnas invalidas'}),400

    if not file or not file.filename.endswith('.csv'):
        return jsonify({'response': 'Solo se aceptan archivos .csv'}), 400
        
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    valid_list = valid_csv(stream,columns)

    stream.seek(0)

    csv_file = csv.reader(stream)

    if valid_list != True:
        return jsonify({'response':'Headers o columnas inválidas en el archivo CSV'}),400
    
    first_row = True
    users_list = []

    if table == 'usuarios':
        users_roles = []

    for row in csv_file:
        if first_row:
            first_row = False
            continue
        
        if table == 'usuarios':
            users_roles.append((row[0],row[-1]))
            del row[-1]

            row[2] = encrypt(row[2])
        users_list.append(tuple(row))

    res = insert_by_csv(users_list,table)
    if res:
        return jsonify({'response':str(res)}),400

    if table == 'usuarios':
        res = insert_by_csv(users_roles,'usuarios_roles')
        if res:
            return jsonify({'response':str(res)}),400

    return jsonify({'response': 'ok', 'data': users_list}), 200

@admin_bp.route('/get-count-roles')
@token_required
@valid_login
@valid_role('get-count-roles')
def get_count_roles():
    student_count = count_students()
    teacher_count = count_teachers()
    admin_count = count_admins()
    users_count = count_users()

    return jsonify({
        'estudiantes': student_count['ammount'],
        'profesores': teacher_count['ammount'],
        'administradores': admin_count['ammount'],
        'usuarios':users_count['ammount']
    })


@admin_bp.route('/update-user',methods = ['PUT'])
@token_required
@valid_login
@valid_role('update-user')
def update_user():
    request_body = request.get_json()

    if not request_body:
        return jsonify({'error': 'No se recibió ningún dato.'}), 400

    user_id = request_body.get('id')
    names = request_body.get('nombres')
    lastnames = request_body.get('apellidos')
    email = request_body.get('correo')
    phone = request_body.get('telefono')

    if not all([user_id, names, lastnames, email, phone]):
        return jsonify({'error': 'Todos los campos son requeridos.'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Correo electrónico no válido.'}), 400

    if not validate_phone(phone):
        return jsonify({'error': 'Número de teléfono no válido.'}), 400

    update_user_info(user_id, names, lastnames, email, phone)

    return jsonify({'success': 'Datos recibidos y validados correctamente.'}), 200


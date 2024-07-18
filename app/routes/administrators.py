import io
import csv
import json
from datetime import datetime

from flask import Blueprint, request, jsonify, session

from ..config import *

from Database import valid_table, TimedeltaEncoder
from Database.encrypt import encrypt
from Database.auth import get_roles
from Database.administrators import *
from Database.students import get_groups_by_students_id
from Database.teachers import get_groups_by_teachers_id, get_all_teachers
from Database.groups import group_exists, insert_group, is_time_overlap

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')

def format_time(time_str:str):
    return datetime.strptime(time_str, '%H:%M').strftime('%H:%M:%S')

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
    users = get_all_users(admin_bp.mysql)
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

        user_info = get_user(admin_bp.mysql, user_id)
        user_roles = get_roles(admin_bp.mysql, user_id)

        if not user_info or not user_roles:
            return jsonify({'error': 'Ha ocurrido un error al obtener la información'}), 404

        roles = [role['id_rol'] for role in user_roles]
        groups = []

        if 3 in roles:
            groups = get_groups_by_students_id(admin_bp.mysql, user_id)
        elif 2 in roles:
            groups = get_groups_by_teachers_id(admin_bp.mysql, user_id)

        groups_json = json.dumps(groups, cls=TimedeltaEncoder)
        groups_json = json.loads(groups_json)

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
    modules = get_all_modules(admin_bp.mysql)
    return jsonify(modules)

@admin_bp.route('/get-teachers')
@token_required
@valid_login
@valid_role('get-teachers')
def get_teachers():
    teachers = get_all_teachers(admin_bp.mysql)
    return jsonify(teachers),200

@admin_bp.route('/get-classrooms')
@token_required
@valid_login
@valid_role('get-classrooms')
def get_classrooms():
    classrooms = get_all_classrooms(admin_bp.mysql)
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

    group = group_exists(admin_bp.mysql,request_body)
    
    if group != None:
        group_json = json.dumps(group, cls=TimedeltaEncoder)
        group_json = json.loads(group_json)
        return jsonify({'error':'El grupo ya existe','info' : group_json }),409

    overlap = is_time_overlap(admin_bp.mysql,request_body['classroom'],request_body['weekday'],request_body['start-time'],request_body['end-time'])
    
    if overlap != None:
        overlap_json = json.dumps(overlap, cls=TimedeltaEncoder)
        overlap_json = json.loads(overlap_json)
        return(jsonify({'error':'Cruce de horarios','info':overlap_json})),409

    res =  insert_group(admin_bp.mysql,request_to_tuple)

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

    res = insert_by_csv(admin_bp.mysql,users_list,table)
    if res:
        return jsonify({'response':str(res)}),400

    if table == 'usuarios':
        res = insert_by_csv(admin_bp.mysql,users_roles,'usuarios_roles')
        if res:
            return jsonify({'response':str(res)}),400

    return jsonify({'response': 'ok', 'data': users_list}), 200

@admin_bp.route('/get-count-roles')
@token_required
@valid_login
@valid_role('get-count-roles')
def get_count_roles():
    student_count = count_students(admin_bp.mysql)
    teacher_count = count_teachers(admin_bp.mysql)
    admin_count = count_admins(admin_bp.mysql)
    users_count = count_users(admin_bp.mysql)

    return jsonify({
        'estudiantes': student_count['ammount'],
        'profesores': teacher_count['ammount'],
        'administradores': admin_count['ammount'],
        'usuarios':users_count['ammount']
    })

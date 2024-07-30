from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.config import valid_role,valid_login
from api.routes import get_now,get_day

from Database.teachers import *
from Database.groups import get_teacher_group,get_group_details
from Database.students import get_students_by_group
from Database.attendances import insert_group_attendance
from Database import encode_time

teachers_bp = Blueprint('teachers',__name__,url_prefix='/teachers')

@teachers_bp.route('/get-teacher-groups')
@jwt_required()
@valid_login
@valid_role('get-teacher-groups')
def get_teacher_groups():

    current_user = get_jwt_identity()

    groups = get_groups_by_teachers_id(current_user['user-id'])
    groups = encode_time(groups)
    return jsonify(groups)


@teachers_bp.route('/get-group-details')
@jwt_required()
@valid_login
@valid_role('get-group-details')
def get_teacher_group_details():
    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')
    
    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta argumentos'}),400
    
    print(group_id,module_id,period)
    group = get_group_details(group_id,module_id,period)

    if group is None:
        return jsonify({'error':'No se encontro un grupo'}),404
    
    group = encode_time(group)
    return jsonify(group),200

@teachers_bp.route('/get-students-by-group')
@jwt_required()
@valid_login
@valid_role('get-students-by-group')
def get_all_students_by_group():
    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')

    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta argumentos'}),400
    
    students = get_students_by_group(group_id,module_id,period)
    
    if not students:
        return jsonify({'response':'No hay estudiantes asignados a este grupo'})
    
    return jsonify(students)

@teachers_bp.route('/set-group-attendance',methods = ['POST'])
@jwt_required()
@valid_login
@valid_role('set-group-attendance')
def set_group_attendance():
    request_body = request.get_json()
    
    group_info = request_body.get('group_info')
    students = request_body.get('students')

    if not group_info or not students:
        return jsonify({'error':'Hacen falta campos'}),400
    
    group_id = group_info.get('group_id')
    module_id = group_info.get('module_id')    
    period = group_info.get('period')

    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta campos'}),400

    if not isinstance(students, list):
        return jsonify({'error': 'Estudiantes inválidos'}), 400       
    
    teacher = get_jwt_identity()
    
    now = get_now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    day = get_day(now.strftime("%A"))  

    #current_time = '08:30:00' 
    
    group = get_teacher_group(teacher['user-id'],group_id,module_id,period,current_time,day) 

    if not group:
        return jsonify({'error':'Grupo no encontrado'}),404
    
    day_info = [current_date,current_time,day]
    res = insert_group_attendance(students,group_id,module_id,period,current_date,current_time)
    
    if res:
        return jsonify({'error':str(res)})

    return jsonify({'data':request_body,'day':day_info})
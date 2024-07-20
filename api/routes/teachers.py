from flask import Blueprint, request, jsonify, session

from api.config import token_required,valid_role,valid_login

from Database.teachers import *
from Database.groups import get_group_details
from Database.students import get_students_by_group
from Database import encode_time

teachers_bp = Blueprint('teachers',__name__,url_prefix='/teachers')

@teachers_bp.route('/get-teacher-groups')
@token_required
@valid_login
@valid_role('get-teacher-groups')
def get_teacher_groups():
    groups = get_groups_by_teachers_id(session['user-id'])
    groups = encode_time(groups)
    return jsonify(groups)


@teachers_bp.route('/get-group-details')
@token_required
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
@token_required
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
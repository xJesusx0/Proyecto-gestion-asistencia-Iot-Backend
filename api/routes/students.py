from flask import Blueprint, request, jsonify, session
from ..config import *
from Database.students import *
from Database.attendances import *
from Database import encode_time
students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/get-student-modules',methods=['GET'])
@token_required
@valid_login
@valid_role('get-student-modules')
def get_modules():

    student_id = session['user-id']
    groups = get_modules_by_id(student_id)    
    return jsonify(groups),200

@students_bp.route('/get-student-attendances-by-group',methods=['GET'])
@token_required
@valid_login
@valid_role('get-student-attendances-by-group')
def get_student_attendances_by_group():
    student_id = session['user-id']
    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')

    if not group_id or not module_id or not period or not student_id:
        return jsonify({'error':'Hacen falta argumentos'}),400
    
    attendances = get_attendances_by_id(student_id,group_id,module_id,period)
    print(attendances)
    if attendances is None:
        return jsonify({'response':'No hay asistencias'})

    attendances_json = encode_time(attendances)

    return jsonify(attendances_json)
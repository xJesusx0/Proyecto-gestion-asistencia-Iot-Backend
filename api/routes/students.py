from flask import Blueprint, request, jsonify, session
from ..config import *
from Database.students import *

students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/get-student-modules',methods=['GET'])
@token_required
@valid_login
@valid_role('get-student-modules')
def get_modules():

    student_id = session['user-id']
    groups = get_modules_by_id(student_id)    
    return jsonify(groups),200


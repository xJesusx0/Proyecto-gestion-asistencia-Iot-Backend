from flask import Blueprint, request, jsonify, session

from api.config import token_required,valid_role,valid_login

from Database.teachers import *
from Database.groups import get_group_details
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
    return 'ok'
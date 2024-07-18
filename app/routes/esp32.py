from datetime import datetime
import json

from flask import Blueprint, request, jsonify, session

from ..config import *
from Database import TimedeltaEncoder
from Database.groups import get_group

esp32_bp = Blueprint('esp32', __name__, url_prefix='/esp32')

def get_day(day_in_english:str):
    days = {
        'Monday': 'lunes',
        'Tuesday': 'martes',
        'Wednesday': 'miércoles',
        'Thursday': 'jueves',
        'Friday': 'viernes',
        'Saturday': 'sábado',
        'Sunday': 'domingo'
    }

    day_in_spanish = days.get(day_in_english,None)

    if day_in_spanish:
        return day_in_spanish
    
    return None

def convert_to_int(number:str):
    try:
        int_number = int(number)
        return int_number

    except ValueError as e:
        print(e)
        return None
    
@esp32_bp.route('/set-attendance',methods = ['POST'])
@token_required
#@valid_login
#@valid_role('get-modules')
def set_attendance():

    request_body = request.get_json()
    print(request_body)

    classroom_id = request_body.get('id_salon',None)
    string_student_id = request_body.get('id_estudiante',None)

    if not classroom_id or not string_student_id:
        return jsonify({'error':'Falta campo id_estudiante o id_salon'}),400

    student_id = convert_to_int(string_student_id)

    if not student_id:
        return jsonify({'error':f'El id de estudiante {string_student_id} tiene un formato incorrecto'}),400

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    day_of_week = now.strftime("%A")

    day = get_day(day_of_week)
    
    # quitar esto 
    current_time = '10:00:00'
    day = 'jueves'
    classroom_id = 4

    group = get_group(esp32_bp.mysql,day,classroom_id,current_time)

    if not group:
        return jsonify({'error':'Ningun grupo asignado a esta hora'}),404

    group_json = json.dumps(group, cls=TimedeltaEncoder)
    group_json = json.loads(group_json)

    group_id = group_json.get('id_grupo')
    module_id = group_json.get('id_modulo')
    period = group_json.get('periodo')

    
    # print(day)
    # print(current_time)
    # print(current_date)
    # print(current_date)

    return jsonify({'response':'ruta del esp','hora':current_time,'fecha':current_date,'dia':day})
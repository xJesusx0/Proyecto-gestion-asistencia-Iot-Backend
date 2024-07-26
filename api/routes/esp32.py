from datetime import datetime
import json

from flask import Blueprint, request, jsonify, session

from ..config import *
from Database import encode_time
from Database.groups import get_group,student_has_group
from Database.attendances import attendance_exists,insert_attendance

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
# @token_required
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
    # current_time = '09:30:00'
    # day = 'miercoles'
    # classroom_id = 3
    # current_date = '2024-07-03'

    group_exists = get_group(day,classroom_id,current_time)

    if not group_exists:
        return jsonify({'error':'Ningun grupo asignado a esta hora'}),404

    group_json = encode_time(group_exists)

    group_id = group_json.get('id_grupo')
    module_id = group_json.get('id_modulo')
    period = group_json.get('periodo')

    has_group = student_has_group(student_id,module_id,period,group_id)

    if not has_group:
        return jsonify({'error':'el usuario no pertenece a este grupo'}),403
    
    exists_attendance = attendance_exists(student_id,group_id,module_id,period,current_date)

    if exists_attendance:
        return jsonify({'response':'El usuario ya tiene una asistencia registrada el dia de hoy'}),409
    
    try:
        insert_attendance(student_id,group_id,module_id,period,current_date,current_time)
    except Exception as e:
        return jsonify({'error':'Ha ocurrido un error'}),500


    return jsonify({'response':'Asistencia insertada correctamente','hora':current_time,'fecha':current_date,'dia':day,'grupo':group_json}),200

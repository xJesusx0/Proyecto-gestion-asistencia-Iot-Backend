from flask import Blueprint, request, jsonify,send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

import dropbox
import io
import csv

from api.config import Config
from api.config import valid_role,valid_login
from api.routes import get_now,get_day

from Database.teachers import *
from Database.groups import get_teacher_group,get_group_details
from Database.students import get_students_by_group
from Database.attendances import insert_group_attendance,get_attendances_by_day,get_students_without_attendance_by_group,count_attendances_by_group
from Database.fails import get_absent_students_by_date,insert_fails,get_fails_by_id_and_group,get_all_fails_by_group,change_approval_state,get_justification_path,count_fails_by_group
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


@teachers_bp.route('/get-students-without-attendance-by-group')
@jwt_required()
@valid_login
@valid_role('get-students-without-attendance-by-group')
def get_students_wo_attendances_by_group():
    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')

    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta argumentos'}),400

    now = get_now()
    current_date = now.strftime("%Y-%m-%d")

    students = get_students_without_attendance_by_group(group_id,module_id,period,current_date)
    
    if not students:
        return jsonify({'response':'No hay estudiantes asignados a este grupo'})
    
    return jsonify(students)

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
        return jsonify({'error':'La clase ya finalizo'}),404
    
    day_info = [current_date,current_time,day]

    for student in students:
        fail_exist = get_fails_by_id_and_group(student,group_id,module_id,period,current_date)
        print(fail_exist)

        if fail_exist:
            return jsonify({'error':f'El estudiante {student} tiene una falla registrada hoy'}),409

    res = insert_group_attendance(students,group_id,module_id,period,current_date,current_time)
    if res:
        if res.args[0] == 1062:
            return jsonify({'error':'asistencias duplicadas'}),409

        return jsonify({'error':str(res)})
    print(res) 
    return jsonify({'data':request_body,'day':day_info})


@teachers_bp.route('/set-group-fails',methods = ['POST'])
@jwt_required()
@valid_login
@valid_role('set-group-fails')
def set_group_fails():
    request_body = request.get_json()
    
    group_info = request_body.get('group_info')

    if not group_info:
        return jsonify({'error':'Hacen falta campos'}),400
    
    group_id = group_info.get('group_id')
    module_id = group_info.get('module_id')    
    period = group_info.get('period')

    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta campos'}),400

    now = get_now()
    current_date = now.strftime("%Y-%m-%d")
    day_of_week = now.strftime("%A")
    day = get_day(day_of_week)
    
    group = get_group_details(group_id,module_id,period)
    print(group)

    if group['dia_semana'] != day:
        return jsonify({'error':'La clase no corresponde al dia de hoy'}),400

    students = get_absent_students_by_date(current_date,group_id,module_id,period) 
    
    if not students:
        return jsonify({'error':'Ha ocurrido un error al obtener los estudiantes'}),404

    students_ids = [student.get('id_estudiante') for student in students]

    res = insert_fails(students_ids,group_id,module_id,period,current_date)
    #res = ''
    if res:
        if res.args[0] == 1062:
            return jsonify({'error':'Ya se han insertado las inasistencias'}),409

        return jsonify({'error':f'Ha ocurrido un error al insertar las inasistencias:\n{res}'}),500
    return jsonify({'response':'ok'})

@teachers_bp.route('/get-day-attendances')
@jwt_required()
@valid_login
@valid_role('get-day-attendances')
def get_day_attendances():

    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')
    
    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta campos'}),400

    now = get_now()
    current_date = now.strftime("%Y-%m-%d")

    attendances = get_attendances_by_day(group_id,module_id,period,current_date)
    if not attendances:
        return jsonify({'error':'No hay asistencias el dia de hoy'}),404

    attendances_json = encode_time(attendances)
    
    return jsonify(attendances_json),200

@teachers_bp.route('/get-fails-by-group')
@jwt_required()
@valid_login
@valid_role('get-fails-by-group')
def get_fails_by_group():

    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')
    
    if not group_id or not module_id or not period:
        return jsonify({'error':'Hacen falta campos'}),400

    fails = get_all_fails_by_group(group_id,module_id,period)
    
    if not fails:
        return jsonify({'error':'No hay inasistencias'}),404

    fails_json = encode_time(fails)

    return jsonify(fails_json)

@teachers_bp.route('/approve-justification',methods = ['POST'])
@jwt_required()
@valid_login
@valid_role('approve-justification')
def aprove_justification():
    request_body = request.get_json()
    
    if not request_body:
        return jsonify({'error':'Hacen falta campos'}),400

    student_id = request_body.get('student_id') 
    group_id = request_body.get('group_id')
    module_id = request_body.get('module_id')    
    period = request_body.get('period')
    date = request_body.get('date')

    if not student_id or not group_id or not module_id or not period or not date:
        return jsonify({'error':'Hacen falta campos'}),400

    res = change_approval_state(student_id,group_id,module_id,period,date)

    if res:
        print(res)
        return jsonify({'error':'Ha ocurrido un error'}),500
    
    return jsonify({'response':'Operacion realizada correctamente'}),200

@teachers_bp.route('/download/<path:filename>')
@jwt_required()
@valid_login
@valid_role('download')
def download_file(filename):
    dbx = dropbox.Dropbox(Config.DROPBOX_SECRET)

    try:
        metadata, response = dbx.files_download('/' + filename)
        
        file_stream = io.BytesIO(response.content)
        print(file_stream)
        print('$$$$$$$$$')        
        return send_file(file_stream, download_name= filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@teachers_bp.route('/get-justification-url')
@jwt_required()
@valid_login
@valid_role('get-justification-url')
def get_justification_url():
    
    student_id =request.args.get('student_id')
    group_id = request.args.get('group_id')
    module_id = request.args.get('module_id')
    period = request.args.get('period')
    date = request.args.get('date')
    
    if not student_id or not group_id or not module_id or not period or not date:
        return jsonify({'error':'Hacen falta campos'}),400

    path = get_justification_path(student_id,group_id,module_id,period,date)

    if not path:
        return jsonify({'error':'No hay una justificacion'}),404
    
    print(path['ruta_archivo'])
    
    return jsonify(path)


@teachers_bp.route('/generate-report',methods = ['POST'])
@jwt_required()
@valid_login
@valid_role('generate-report')
def generate_report():
    request_body = request.get_json()
    
    if not request_body:
        return jsonify({'error':'Hacen falta campos'}),400

    group_id = request_body.get('group_id')
    module_id = request_body.get('module_id')    
    period = request_body.get('period')

    if not group_id or not module_id or not period: 
        return jsonify({'error':'Hacen falta campos'}),400

    fails = count_fails_by_group(group_id,module_id,period)
    attendances = count_attendances_by_group(group_id,module_id,period)
    students = get_students_by_group(group_id,module_id,period)
    
    data = {
        'estudiantes':students,
        'asistencias':attendances,
        'inasistencias':fails
    }

    students_dict = {student['id_estudiante']: student for student in data['estudiantes']}

    for student in students_dict.values():
        student['asistencias'] = 0
        student['faltas'] = 0

    if data['asistencias']:

        for asistencia in data['asistencias']:
            student_id = asistencia['id_estudiante']
            if student_id in students_dict:
                students_dict[student_id]['asistencias'] += asistencia['asistencias']

    if data['inasistencias']:

        for inasistencia in data['inasistencias']:
            student_id = inasistencia['id_estudiante']
            if student_id in students_dict:
                students_dict[student_id]['faltas'] = inasistencia['inasistencias']

    resultado = [
        {
            'id_estudiante': est['id_estudiante'],
            'nombre': est['nombres'],
            'apellido': est['apellidos'],
            'asistencias': est['asistencias'],
            'faltas': est['faltas']
        }
        for est in students_dict.values()
    ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=resultado[0].keys())
    
    writer.writeheader()
    writer.writerows(resultado)
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='data.csv'
    )
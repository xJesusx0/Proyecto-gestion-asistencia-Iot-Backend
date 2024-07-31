from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import dropbox

from ..config import *
from Database.students import *
from Database.attendances import *
from Database import encode_time

students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/get-student-modules',methods=['GET'])
# @token_required
@valid_login
@valid_role('get-student-modules')
def get_modules():

    current_user = get_jwt_identity()
    student_id = current_user['user-id']
    groups = get_modules_by_id(student_id)    
    return jsonify(groups),200

@students_bp.route('/get-student-attendances-by-group',methods=['GET'])
@jwt_required()
@valid_login
@valid_role('get-student-attendances-by-group')
def get_student_attendances_by_group():

    current_user = get_jwt_identity()

    student_id = request.args.get('student_id')
    print(student_id)

    if not student_id or student_id == 'null':
        student_id = current_user['user-id']
    print('$$$$$$$$$$$$$')
    print(student_id)
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

@students_bp.route('/set-justification',methods=['POST'])
@jwt_required()
@valid_login
@valid_role('set-justification')
def set_justification():
    
    if 'file' not in request.files:
        return jsonify({'error':'se esperaba un archivo'}),400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'response': 'No se selecciono un archivo'}), 400

    if not file:
        return jsonify({'response': 'No se selecciono un archivo'}), 400

    MAX_FILE_SIZE = 2 * 1024 * 1024

    file.seek(0, os.SEEK_END) 
    file_size = file.tell()   
    file.seek(0)           

    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'El archivo es demasiado grande'}), 400

    valid_extensions = {'.png', '.jpg', '.pdf','.jpeg'}

    if hasattr(file, 'filename') and file.filename:
        filename = file.filename.lower()
        
        extension = os.path.splitext(filename)[1]

        valid_type = extension in valid_extensions
    else:
        valid_type = False

    if not valid_type:
        return jsonify({'error': 'Formato de archivo invalido'}), 400

    dbx = dropbox.Dropbox(Config.DROPBOX_SECRET)
   
    dropbox_path = f'/{file.filename}'

    try:    
        file_data = file.read()
        response = dbx.files_upload(file_data, dropbox_path)
        print(f'Archivo subido exitosamente: {response.name}')
    except Exception as e:
        print(f'Error al subir el archivo: {e}')

    return jsonify({'response':'ok'})


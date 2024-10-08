from Database import handle_database_operations

@handle_database_operations
def insert_group(mysql,cursor,group:tuple):
    print(tuple)
    try:
        cursor.execute('INSERT INTO grupo (id_grupo, id_modulo, id_profesor, id_salon, periodo, dia_semana, hora_inicio, hora_fin ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',group)
        return 'ok'
    
    except Exception as e:
        return str(e)
    

@handle_database_operations
def group_exists(mysql,cursor,group:dict):
    info = (group['module'],group['classroom'],group['period'],group['weekday'],group['start-time'],group['end-time'])

    cursor.execute('SELECT * FROM grupo WHERE id_modulo = %s AND id_salon = %s AND periodo = %s AND dia_semana = %s AND hora_inicio = %s AND hora_fin = %s',info)
    res = cursor.fetchall()
    if res:
        return res
    
    return None

@handle_database_operations
def is_time_overlap(mysql, cursor, classroom, weekday, start_time, end_time):
    query = """
    SELECT * FROM grupo
    WHERE id_salon = %s
    AND dia_semana = %s
    AND (
        (%s < hora_fin AND %s > hora_inicio) OR
        (%s < hora_fin AND %s > hora_inicio)
    )
    LIMIT 1
    """

    cursor.execute(query,(classroom, weekday, start_time, start_time, end_time, end_time))
    res = cursor.fetchall()

    if res:
        return res
    
    return None

@handle_database_operations
def get_group(mysql,cursor,day:str,classroom_id:int,time:str):
    cursor.execute('SELECT * FROM grupo WHERE id_salon = %s AND dia_semana = %s AND hora_inicio <= %s AND hora_fin >= %s',(classroom_id,day,time,time))
    response = cursor.fetchone()

    if response:
        return response
    
    return None

@handle_database_operations
def student_has_group(mysql,cursor,student_id,module_id,period,group_id):
    cursor.execute('select * from matricula where id_estudiante = %s AND id_modulo = %s and periodo = %s and id_grupo = %s',(student_id,module_id,period,group_id))
    response = cursor.fetchall()
    if response:
        return response
    
    return None

@handle_database_operations
def get_group_details(mysql,cursor,group_id,module_id,period):
    cursor.execute('select grupo.*,modulos.nombre,salones.nombre,salones.sede from grupo join modulos on grupo.id_modulo = modulos.id_modulo join salones on grupo.id_salon = salones.id_salon where grupo.id_grupo = %s AND grupo.id_modulo = %s AND periodo = %s',(group_id,module_id,period))
    response = cursor.fetchone()
    if response:
        return response
    
    return None

@handle_database_operations
def insert_students_to_group(mysql,cursor,group_id:str,module_id:str,period:str,students_ids:tuple):
    
    data = [(group_id,module_id,period,student_id) for student_id in students_ids]

    query = 'INSERT INTO matricula (id_grupo, id_modulo, periodo, id_estudiante) VALUES (%s, %s, %s, %s)'

    try:
        cursor.executemany(query,data)
    except Exception as e:
        return e
    
@handle_database_operations
def get_all_groups(mysql,cursor):
    cursor.execute('SELECT grupo.*,modulos.nombre FROM grupo JOIN modulos ON grupo.id_modulo = modulos.id_modulo')
    res = cursor.fetchall()
    if res:
        return res
    
    return None

@handle_database_operations
def get_students_not_in_group(mysql,cursor,group_id,module_id,period):
    cursor.execute('select estudiante.id_estudiante,usuarios.nombres,usuarios.apellidos from estudiante left join matricula on matricula.id_estudiante = estudiante.id_estudiante and matricula.id_grupo = %s and matricula.id_modulo = %s and periodo = %s join usuarios on estudiante.id_estudiante = usuarios.id_usuario where matricula.id_estudiante is null',(group_id,module_id,period))
    res = cursor.fetchall()
    if res:
        return res
    
    return None

@handle_database_operations
def get_teacher_group(mysql,cursor,teacher_id,group_id,module_id,period,time,day):
    
    cursor.execute('SELECT * FROM grupo where id_profesor = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s AND %s >= hora_inicio and %s <= hora_fin AND dia_semana = %s',(teacher_id,group_id,module_id,period,time,time,day))
    res = cursor.fetchone()

    if res:
        return res
    
    return None 
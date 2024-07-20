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
    cursor.execute('select grupo.*,modulos.nombre,salones.nombre,salones.sede from grupo join modulos on grupo.id_modulo = modulos.id_modulo join salones on grupo.id_salon = salones.id_salon where group.id_grupo = %s AND group.id_modulo = %s AND periodo = %s',(group_id,module_id,period))
    response = cursor.fetchall()
    return response
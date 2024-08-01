from Database import handle_database_operations

@handle_database_operations
def attendance_exists(mysql,cursor,student_id,group_id,module_id,period,date):
    cursor.execute('SELECT * FROM asistencias WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s AND fecha = %s',(student_id,group_id,module_id,period,date))

    response = cursor.fetchall()
    if response:
        return response
    
    return None

@handle_database_operations
def get_attendances_by_id(mysql,cursor,student_id,group_id,module_id,period):
    cursor.execute('SELECT * from asistencias WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s',(student_id,group_id,module_id,period))
    response = cursor.fetchall()
    if response:
        return response
        
    return None
@handle_database_operations
def insert_attendance(mysql,cursor,student_id,group_id,module_id,period,date,time):
    cursor.execute('INSERT INTO asistencias (id_estudiante, id_grupo, id_modulo, periodo, fecha, hora_llegada) VALUES (%s, %s, %s, %s, %s, %s)',(student_id,group_id,module_id,period,date,time))

@handle_database_operations
def insert_group_attendance(mysql,cursor,students_list,group_id,module_id,period,date,time):
    
    query = 'INSERT INTO asistencias (id_estudiante,id_grupo,id_modulo,periodo,fecha,hora_llegada) VALUES (%s,%s,%s,%s,%s,%s)'
    data = [(student_id,group_id,module_id,period,date,time) for student_id in students_list]

    try:
        cursor.executemany(query,data)
    except Exception as e:
        return e

@handle_database_operations
def get_attendances_by_day(mysql,cursor,group_id,module_id,period,date):
    cursor.execute('select asistencias.*,usuarios.nombres,usuarios.apellidos from asistencias join usuarios on usuarios.id_usuario = asistencias.id_estudiante where id_grupo = %s and id_modulo = %s and periodo = %s and fecha = %s order by asistencias.hora_llegada',(group_id,module_id,period,date))
    res = cursor.fetchall()
    if res:
        return res
    
    return None

@handle_database_operations
def get_students_without_attendance_by_group(mysql,cursor,group_id,module_id,period,date):
    
    query = """
        SELECT matricula.id_estudiante, usuarios.nombres,usuarios.apellidos FROM matricula 
        JOIN usuarios ON matricula.id_estudiante = usuarios.id_usuario 
        LEFT JOIN asistencias  ON matricula.id_estudiante = asistencias.id_estudiante
        AND asistencias.id_grupo = matricula.id_grupo    
        AND asistencias.id_modulo = matricula.id_modulo    
        AND asistencias.periodo = matricula.periodo    
        AND asistencias.fecha = %s 
        WHERE matricula.id_grupo = %s   
        AND matricula.id_modulo = %s 
        AND matricula.periodo = %s
        AND asistencias.id_estudiante IS NULL;            
        """

    values = (date,group_id,module_id,period)


    cursor.execute(query,values)
    res = cursor.fetchall()
    if res:
        return res
    
    return None
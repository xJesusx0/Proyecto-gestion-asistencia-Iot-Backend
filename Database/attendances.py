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
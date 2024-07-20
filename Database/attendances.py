from Database import handle_database_operations

@handle_database_operations
def attendance_exists(mysql,cursor,student_id,group_id,module_id,period,date):
    cursor.execute('SELECT * FROM asistencias WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s AND fecha = %s',(student_id,group_id,module_id,period,date))

    response = cursor.fetchall()
    if response:
        return response
    
    return None

@handle_database_operations
def insert_attendance(mysql,cursor,student_id,group_id,module_id,period,date,time):
    return 'ok'
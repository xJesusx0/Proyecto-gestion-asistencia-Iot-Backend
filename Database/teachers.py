from Database import handle_database_operations

@handle_database_operations
def get_groups_by_teachers_id(mysql,cursor,teacher_id:str):
    cursor.execute('SELECT * FROM grupo WHERE id_profesor = %s',(teacher_id,))
    response = cursor.fetchall()
    return response

@handle_database_operations
def get_all_teachers(mysql,cursor):
    cursor.execute('SELECT usuarios.id_usuario,usuarios.nombres,usuarios.apellidos FROM profesor JOIN usuarios ON id_usuario = id_profesor')
    response = cursor.fetchall()
    return response
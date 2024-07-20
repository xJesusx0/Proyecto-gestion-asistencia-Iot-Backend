from Database import handle_database_operations

@handle_database_operations
def get_modules_by_id(mysql,cursor,student_id:str):

    cursor.execute('SELECT * FROM modulos JOIN matricula ON matricula.id_modulo = modulos.id_modulo WHERE matricula.id_estudiante = %s',(student_id,))
    response = cursor.fetchall()
    return response


@handle_database_operations
def get_groups_by_students_id(mysql,cursor,student_id:str):
    cursor.execute('select * from grupo where id_grupo in (select id_grupo from matricula where id_estudiante = %s)',(student_id,))
    response = cursor.fetchall()
    return response

@handle_database_operations
def get_students_by_group(mysql,cursor,group_id,module_id,period):
    cursor.execute('select matricula.*,usuarios.nombres,usuarios.apellidos,usuarios.id_usuario,usuarios.correo from matricula join usuarios on matricula.id_estudiante = usuarios.id_usuario where id_grupo = %s and id_modulo = %s and periodo = %s',(group_id,module_id,period))
    response = cursor.fetchall()
    return response
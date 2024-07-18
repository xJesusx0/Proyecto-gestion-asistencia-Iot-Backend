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
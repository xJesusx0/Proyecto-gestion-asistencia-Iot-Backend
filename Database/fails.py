from Database import handle_database_operations


@handle_database_operations
def get_absent_students_by_date(mysql,cursor,date,group_id,module_id,period):

    query = """
    select estudiante.id_estudiante from estudiante left join asistencias on estudiante.id_estudiante = asistencias.id_estudiante 
    and fecha = %s 
    join matricula on estudiante.id_estudiante = matricula.id_estudiante 
    where matricula.id_grupo = %s
    and matricula.id_modulo = %s
    and matricula.periodo = %s 
    and asistencias.id_estudiante is null
    """

    cursor.execute(query,(date,group_id,module_id,period))

    res = cursor.fetchall()

    if res:
        return res
    
    return None

@handle_database_operations
def insert_fails(mysql,cursor,students_ids,group_id,module_id,period,date):

    query = 'INSERT INTO inasistencia (id_estudiante,id_grupo,id_modulo,periodo,fecha) values (%s,%s,%s,%s,%s)'

    values = [(student_id,group_id,module_id,period,date) for student_id in students_ids]

    print(values)

    try:
        cursor.executemany(query,values)
    except Exception as e:
        return e
    
@handle_database_operations
def get_fails_by_student(mysql,cursor,student_id):
    cursor.execute('SELECT inasistencia.*, modulos.nombre FROM inasistencia join modulos on inasistencia.id_modulo = modulos.id_modulo WHERE id_estudiante = %s',(student_id,))

    res = cursor.fetchall()
    if res:
        return res
    
    return None

@handle_database_operations
def insert_justification(mysql,cursor,student_id,group_id,module_id,period,date,url,description):

    query = 'INSERT INTO justificaciones (id_estudiante,id_grupo,id_modulo,periodo,fecha,ruta_archivo,descripcion) values (%s,%s,%s,%s,%s,%s,%s)'
    values = (student_id,group_id,module_id,period,date,url,description)
    try:
        cursor.execute(query,values)
    except Exception as e:
        return e

@handle_database_operations
def get_fails_by_id_and_group(mysql,cursor,student_id,group_id,module_id,period,date):
    cursor.execute('SELECT * FROM inasistencia WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s AND fecha = %s',(student_id,group_id,module_id,period,date))

    res = cursor.fetchall()

    if res:
        return res

    return None

@handle_database_operations
def get_fails_by_id_and_group_(mysql,cursor,student_id,group_id,module_id,period):
    cursor.execute('SELECT * FROM inasistencia WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s ',(student_id,group_id,module_id,period))

    res = cursor.fetchall()

    if res:
        return res

    return None
@handle_database_operations
def get_all_fails_by_group(mysql,cursor,group_id,module_id,period):
    cursor.execute('SELECT inasistencia.*,usuarios.nombres,usuarios.apellidos FROM inasistencia JOIN usuarios on usuarios.id_usuario = inasistencia.id_estudiante WHERE id_grupo = %s AND id_modulo = %s AND periodo = %s ORDER BY justificada desc',(group_id,module_id,period))

    res = cursor.fetchall()

    if res:
        return res

    return None

@handle_database_operations
def change_justification_state(mysql,cursor,student_id,group_id,module_id,period,date):
    try: 
        cursor.execute('UPDATE inasistencia SET justificada = 1 WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s AND fecha = %s',(student_id,group_id,module_id,period,date))
    except Exception as e:
        return e

@handle_database_operations
def change_approval_state(mysql,cursor,student_id,group_id,module_id,period,date):
    try: 
        cursor.execute('UPDATE inasistencia SET aprobada = 1 WHERE id_estudiante = %s AND id_grupo = %s AND id_modulo = %s AND periodo = %s AND fecha = %s',(student_id,group_id,module_id,period,date))
    except Exception as e:
        return e
    
@handle_database_operations
def get_justification_path(mysql,cursor,student_id,group_id,module_id,period,date):

    cursor.execute('select * from justificaciones where id_estudiante = %s and id_grupo = %s and id_modulo = %s and periodo = %s and fecha = %s',(student_id,group_id,module_id,period,date))

    res = cursor.fetchone()

    if res:
        return res
    
    return None


@handle_database_operations
def count_fails_by_group(mysql,cursor,group_id,module_id,period):
    cursor.execute('select id_estudiante,count(*) as inasistencias from inasistencia where id_grupo = %s and id_modulo = %s and periodo = %s group by id_estudiante',(group_id,module_id,period))

    res = cursor.fetchall()
    if res:
        return res
    
    return None


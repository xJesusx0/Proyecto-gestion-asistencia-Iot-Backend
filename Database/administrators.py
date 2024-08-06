from Database import handle_database_operations

from Database.encrypt import encrypt

@handle_database_operations
def get_all_users(mysql,cursor):
    cursor.execute('SELECT id_usuario, correo, nombres, apellidos, numero_telefonico FROM usuarios')
    response = cursor.fetchall()
    return response

@handle_database_operations
def get_user(mysql,cursor,user_id):
    cursor.execute('SELECT id_usuario, correo, nombres, apellidos, numero_telefonico FROM usuarios WHERE id_usuario = %s',(user_id,))
    response = cursor.fetchall()
    return response

@handle_database_operations
def count_students(mysql,cursor):
    cursor.execute('SELECT COUNT(*) as ammount FROM usuarios_roles WHERE id_rol = 3')
    
    response = cursor.fetchone()
    if response:
        return response

    return None

@handle_database_operations
def count_teachers(mysql,cursor):
    cursor.execute('SELECT COUNT(*) as ammount FROM usuarios_roles WHERE id_rol = 2')
    
    response = cursor.fetchone()
    if response:
        return response

    return None

@handle_database_operations
def count_admins(mysql,cursor):
    cursor.execute('SELECT COUNT(*) as ammount FROM usuarios_roles WHERE id_rol = 1')
    response = cursor.fetchone()

    if response:
        return response

    return None

@handle_database_operations
def count_users(mysql,cursor):
    cursor.execute('SELECT COUNT(*) as ammount FROM usuarios')
    response = cursor.fetchone()
    if response:
        return response

    return None

@handle_database_operations
def get_all_modules(mysql,cursor):
    cursor.execute('SELECT * FROM modulos')
    response = cursor.fetchall()
    return response

@handle_database_operations
def get_all_classrooms(mysql,cursor):
    cursor.execute('SELECT * FROM salones')
    response = cursor.fetchall()
    return response

@handle_database_operations
def insert_by_csv(mysql,cursor,users_list:tuple,tablename:str):
    print(tablename)

    querys = {
        'usuarios':'INSERT INTO usuarios (id_usuario,correo,contraseña, nombres, apellidos,numero_telefonico) VALUES (%s,%s,%s,%s,%s,%s)',
        'estudiante': 'INSERT INTO estudiante (id_estudiante, id_programa, cuatrimestre) VALUES (%s, %s, %s)',
        'profesor': 'INSERT INTO profesor (id_profesor) VALUES (%s)',
        'usuarios_roles': 'INSERT INTO usuarios_roles (id_usuario, id_rol) VALUES (%s, %s)'

    }

    query = querys.get(tablename,None)
    if query == None:
        raise ValueError('Nombre de tabla invalida')
    try:
        cursor.executemany(query,users_list)
    except Exception as e:
        return e
    
@handle_database_operations
def update_user_info(mysql,cursor,user_id, names, lastnames, email, phone):
    cursor.execute('UPDATE usuarios SET nombres = %s, apellidos = %s, correo = %s, numero_telefonico = %s WHERE id_usuario = %s',(names,lastnames,email,phone,user_id))

    return 'ok1'

@handle_database_operations
def get_attendances_by_weekday(mysql,cursor):
    cursor.execute('SELECT grupo.dia_semana, COUNT(*) AS cantidad_asistencias FROM asistencias JOIN grupo ON grupo.id_grupo = asistencias.id_grupo GROUP BY grupo.dia_semana ORDER BY cantidad_asistencias DESC')
    response = cursor.fetchall()

    return response

@handle_database_operations
def count_students_by_group(mysql,cursor):
    cursor.execute('select grupo.id_grupo, count(*) as cantidad_estudiante FROM matricula join grupo on grupo.id_grupo = matricula.id_grupo group by grupo.id_grupo order by cantidad_estudiante desc')
    response = cursor.fetchall()
    return response

@handle_database_operations
def count_groups_by_module(mysql,cursor):
    query = "SELECT m.nombre AS modulo, COUNT(g.id_grupo) AS total_grupos FROM grupo g JOIN modulos m ON g.id_modulo = m.id_modulo GROUP BY m.nombre"
    cursor.execute(query)
    response = cursor.fetchall()
    return response

@handle_database_operations
def fails_by_module(mysql,cursor):
    query = 'SELECT m.nombre AS modulo, COUNT(i.id_estudiante) AS total_inasistencias FROM inasistencia i JOIN modulos m ON i.id_modulo = m.id_modulo GROUP BY m.id_modulo ORDER BY total_inasistencias DESC'
    cursor.execute(query)
    response = cursor.fetchall()
    return response

@handle_database_operations
def count_justificated_and_no_justifiacted_fails(mysql,cursor):
    query = 'SELECT SUM(CASE WHEN i.justificada = 1 THEN 1 ELSE 0 END) AS inasistencias_justificadas, SUM(CASE WHEN i.justificada = 0 THEN 1 ELSE 0 END) AS inasistencias_no_justificadas FROM inasistencia i'
    cursor.execute(query)
    response = cursor.fetchall()
    return response



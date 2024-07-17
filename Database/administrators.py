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
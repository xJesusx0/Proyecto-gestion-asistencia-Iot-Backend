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
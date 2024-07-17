from Database import handle_database_operations

from Database.encrypt import decrypt

@handle_database_operations
def validateLogin(mysql,cursor,user_data:dict):
    username = user_data['username']
    password = user_data['password']

    print(user_data)

    cursor.execute('SELECT * FROM usuarios WHERE correo = %s;',(username,))
    response = cursor.fetchone()
    print('res',response)
    if response:
        stored_password_hash = response['contraseña']
        if decrypt(password,stored_password_hash):
            return response


    return None

@handle_database_operations
def get_roles(mysql,cursor,user_id:int):
    cursor.execute('SELECT id_usuario,usuarios_roles.id_rol,nombre FROM usuarios_roles JOIN roles ON roles.id_rol = usuarios_roles.id_rol WHERE usuarios_roles.id_usuario = %s ;',(user_id,))

    response = cursor.fetchall()
    return response

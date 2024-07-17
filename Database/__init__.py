from functools import wraps
from MySQLdb.cursors import DictCursor
import json
from datetime import timedelta

def handle_database_operations(func: callable) -> callable:
    @wraps(func)
    def wrapper(mysql, *args, **kwargs):
        cursor = mysql.connection.cursor(DictCursor)
        try:
            result = func(mysql, cursor, *args, **kwargs)
            mysql.connection.commit()
            return result
        except Exception as error:
            mysql.connection.rollback()
            print("Database error:", error)
        finally:
            cursor.close()
    return wrapper

def valid_table(tablename:str):
    tables = {
        'usuarios':{'id_usuario','correo','contraseña','nombres','apellidos','numero_telefonico','id_rol'},
        'estudiantes':{'id_estudiante','programa'},
        'profesor':{'id_profesor'}
    }
    

    fields = tables.get(tablename,None)

    if fields != None:
        return fields
    
    return None

class TimedeltaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)

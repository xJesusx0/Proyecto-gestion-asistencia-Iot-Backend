from functools import wraps
import json

from pymysql.cursors import DictCursor 
import pymysql
from datetime import timedelta
from api.config import Config

def get_db_connection():
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        cursorclass=DictCursor
    )
    return connection


def handle_database_operations(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            result = func(connection, cursor, *args, **kwargs)
            connection.commit()
            return result
        except Exception as error:
            connection.rollback()
            print("error:", error)
        finally:
            cursor.close()
            connection.close()
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

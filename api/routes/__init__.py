import os
import json
import pytz

from datetime import datetime

current_dir = os.path.dirname(__file__)

web_routes_file = os.path.join(current_dir, '../../json/web-routes.json')
api_routes_file = os.path.join(current_dir, '../../json/api-routes.json')

web_routes_route = os.path.abspath(web_routes_file)
api_routes_route = os.path.abspath(api_routes_file)

web_routes = {}
api_routes = {}

if not os.path.exists(web_routes_route):
    print(f"El archivo '{web_routes_file}' no existe.")

if not os.path.exists(api_routes_route):
    print(f"El archivo '{api_routes_file}' no existe.")
        
with open(web_routes_route, 'r') as f:
    web_routes = json.load(f)

with open(api_routes_route, 'r') as f:
    api_routes = json.load(f)

def get_day(day_in_english:str):
    days = {
        'Monday': 'lunes',
        'Tuesday': 'martes',
        'Wednesday': 'miércoles',
        'Thursday': 'jueves',
        'Friday': 'viernes',
        'Saturday': 'sábado',
        'Sunday': 'domingo'
    }

    day_in_spanish = days.get(day_in_english,None)

    if day_in_spanish:
        return day_in_spanish
    
    return None

def get_now():
    bogota_tz = pytz.timezone('America/Bogota')

    now = datetime.now(bogota_tz) 
    return now
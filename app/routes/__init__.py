import os
import json

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


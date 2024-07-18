from flask import Flask,jsonify
from flask_cors import CORS
from flask_session import Session

import pymysql

from api.config import Config

from api.routes.auth import auth_bp
from api.routes.administrators import admin_bp
from api.routes.students import students_bp
from api.routes.esp32 import esp32_bp

app = Flask(__name__)

app.config.from_object(Config)

Session(app)
CORS(app, supports_credentials=True)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error':404,'response':'Ruta no encontrada'}), 404

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(students_bp)
app.register_blueprint(esp32_bp)
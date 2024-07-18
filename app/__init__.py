from flask import Flask,jsonify
from flask_cors import CORS
from flask_session import Session
from flask_mysqldb import MySQL

from app.config import Config

from app.routes.auth import auth_bp
from app.routes.administrators import admin_bp
from app.routes.students import students_bp
from app.routes.esp32 import esp32_bp

app = Flask(__name__)

app.config.from_object(Config)

Session(app)
CORS(app, supports_credentials=True)
mysql = MySQL(app)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error':404,'response':'Ruta no encontrada'}), 404

auth_bp.mysql = mysql
admin_bp.mysql = mysql
students_bp.mysql = mysql
esp32_bp.mysql = mysql

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(students_bp)
app.register_blueprint(esp32_bp)
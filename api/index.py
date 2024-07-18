from flask import Flask
from flask_cors import CORS
from flask_session import Session
import os
from flask_mysqldb import MySQL
from api.config import Config

from api.routes.auth import auth_bp
from api.routes.administrators import admin_bp
from api.routes.students import students_bp

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = 'secret'

Session(app)
CORS(app, supports_credentials=True)
mysql = MySQL(app)

@app.route('/')
def index():
    return 'hola mundo'

auth_bp.mysql = mysql
admin_bp.mysql = mysql
students_bp.mysql = mysql
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(students_bp)
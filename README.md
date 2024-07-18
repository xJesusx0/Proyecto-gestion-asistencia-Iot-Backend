# Proyecto de Gestión de Asistencia mediante IoT

Este proyecto utiliza tecnología IoT para gestionar y monitorizar la asistencia de manera eficiente.

## Requisitos Previos

- [XAMPP](https://www.apachefriends.org/index.html) instalado
- [Git](https://git-scm.com/) instalado
- [Python 3](https://www.python.org/downloads/) instalado
- [MySQL](https://www.mysql.com/) incluido en XAMPP

## Instalación y Configuración

### Configuración del Backend

1. **Crear un entorno virtual en Python:**
   ```bash
   python3 -m venv env
   ```

2. **Activar el entorno virtual:**

   - En Linux:
     ```bash
     source env/bin/activate
     ```
   - En Windows:
     ```cmd
     .\env\Scripts\activate
     ```

3. **Instalar las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos MySQL:**

   - Abre el cliente MySQL desde XAMPP.
   - Crear y usar la base de datos:
     ```sql
     CREATE DATABASE proyecto;
     USE proyecto;
     ```
   - Importar la base de datos:
     - Desde el cliente MySQL en Linux:
      ```sql
      SOURCE /opt/lampp/htdocs/Proyecto-gestion-asistencia-Iot/Backend/Database/Proyecto.sql;
      ```

5. ** a `config.py`:**

   - Dirígete a la siguiente ruta:
     ```bash
     cd Proyecto-gestion-asistencia-Iot/Backend/app/
     ```
   - Crea el archivo de configuración `.env`:
     ```
      MYSQL_HOST = localhost #Tu host
      MYSQL_USER = root # Tu usuario (por defecto es root)
      MYSQL_DB = nombre_db # El nombre de la base de datos
      SECRET_KEY = secret # una clave secreta (por defecto es secret)
      MYSQL_PASSWORD = contraseña # Tu contraseña de mysql
      SECRET_TOKEN = token # token de autentificacion (por defecto es 1234)
     ```

6. **Iniciar el backend:**
   ```bash
   python3 Backend/run.py
   ```
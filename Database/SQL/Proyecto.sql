CREATE TABLE facultades (
  id_facultad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  decano VARCHAR(100)
);

CREATE TABLE programas (
  id_programa INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  fkid_facultad INT,
  lugar_de_oferta VARCHAR(100),
  modalidad VARCHAR(100),
  duracion INT,
  FOREIGN KEY (fkid_facultad) REFERENCES facultades(id_facultad)
);

CREATE TABLE modulos (
  id_modulo VARCHAR(100) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  creditos INT
);

CREATE TABLE roles (
  id_rol INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(100)
);

CREATE TABLE usuarios (
  id_usuario VARCHAR(40) PRIMARY KEY,
  correo VARCHAR(100) UNIQUE NOT NULL,
  contraseña VARCHAR(100) NOT NULL,
  nombres VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  numero_telefonico VARCHAR(100)
);

CREATE TABLE usuarios_roles (
  id_usuario VARCHAR(40),
  id_rol INT,
  PRIMARY KEY (id_usuario, id_rol),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
  FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

CREATE TABLE profesor (
  id_profesor VARCHAR(40) PRIMARY KEY,
  -- especialidad VARCHAR(100),
  FOREIGN KEY (id_profesor) REFERENCES usuarios(id_usuario)
);

CREATE TABLE estudiante (
  id_estudiante VARCHAR(40) PRIMARY KEY,
  id_programa INT,
  FOREIGN KEY (id_estudiante) REFERENCES usuarios(id_usuario),
  FOREIGN KEY (id_programa) REFERENCES programas(id_programa)
);

CREATE TABLE salones (
  id_salon INT AUTO_INCREMENT PRIMARY KEY,
  sede VARCHAR(100) NOT NULL,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE grupo (
  id_grupo VARCHAR(100),
  id_modulo VARCHAR(100),
  id_profesor VARCHAR(40),
  id_salon INT,
  periodo VARCHAR(100),
  dia_semana VARCHAR(50),
  hora_inicio TIME,
  hora_fin TIME,
  PRIMARY KEY (id_grupo, id_modulo, periodo),
  FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo),
  FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor),
  FOREIGN KEY (id_salon) REFERENCES salones(id_salon)
);


CREATE TABLE matricula (
  id_grupo VARCHAR(100),
  id_modulo VARCHAR(100),
  periodo VARCHAR(40),
  id_estudiante VARCHAR(40),
  PRIMARY KEY (id_grupo, id_modulo,periodo,id_estudiante),
  FOREIGN KEY (id_grupo) REFERENCES grupo(id_grupo),
  FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante)
);

CREATE TABLE asistencias (
  id_estudiante VARCHAR(40),
  id_grupo VARCHAR(100),
  id_modulo VARCHAR(100),
  periodo VARCHAR(100),
  fecha DATE,
  hora_llegada TIME,
  PRIMARY KEY (id_estudiante, id_grupo, id_modulo, periodo, fecha),
  FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante),
  FOREIGN KEY (id_grupo) REFERENCES grupo(id_grupo),
  FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo)
);


CREATE TABLE tipo_de_inasistencia (
  id_tipo INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255)
);

CREATE TABLE inasistencia (
  id_inasistencia INT AUTO_INCREMENT PRIMARY KEY,
  id_grupo VARCHAR(100),
  id_estudiante VARCHAR(40),
  fecha DATE,
  id_tipo INT,
  FOREIGN KEY (id_grupo) REFERENCES grupo(id_grupo),
  FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante),
  FOREIGN KEY (id_tipo) REFERENCES tipo_de_inasistencia(id_tipo)
);

CREATE TABLE justificaciones (
  id_justificacion INT PRIMARY KEY,
  ruta_archivo VARCHAR(255),
  id_inasistencia INT,
  descripcion VARCHAR(255),
  FOREIGN KEY (id_inasistencia) REFERENCES inasistencia(id_inasistencia)
);
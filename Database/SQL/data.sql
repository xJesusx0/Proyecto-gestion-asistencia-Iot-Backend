INSERT INTO roles (nombre, descripcion) 
VALUES  
    ('Administrador', 'Rol con permisos administrativos'),
    ('Profesor', 'Rol para los profesores'),
    ('Estudiante', 'Rol para los estudiantes');

insert into facultades(nombre,decano) values ('Ingenierias','Piedad Marchena Villanueva');

insert into programas (nombre,fkid_facultad,lugar_de_oferta,modalidad,duracion) values ('Técnica Profesional en Mantenimiento de Sistemas Informáticos',1,'Soledad','Presencial',5);

INSERT INTO usuarios (id_usuario, correo, contraseña, nombres, apellidos, numero_telefonico)
VALUES
    ('1234', 'jalbertoperea@unibarranquilla.edu.co','$2b$12$WRuuBqRyibTCehiNljjcC.hOdgC/s4pssLCOn0w2/tisdSCJyNkTu', 'Jesus Alberto', 'Perea Linares', '123456789'),
    ('1237', 'mdsolis@unibarranquilla.edu.co','$2b$12$g.JWyTfs0.dr0L1gNGxTR.Y93XTgZndPbJGFf9Y3X5JpKG1wbqb5.', 'Moises David', 'Solis Morrillo', '234567891'),
    ('1235', 'acarlosperez@unibarranquilla.edu.co', '$2b$12$Gox9y./ydRMZf4Hquxks4uwbd9uyGhDmASFHyzeUwANPNrGpTD1Jy', 'Alberto Carlos', 'Perez Rivera', '3456789012'),
    ('1236', 'ddussan@unibarranquilla.edu.co', '$2b$12$nLFQOlfcg2uX4arNzzUH1e4BemX/akJ2AIB69P9TlfXG8mR3wQyye', 'Daniel David', 'Dussan Gonzalez', '4567890123'),
    ('1238', 'bjfernandez@unibarranquilla.edu.co', '$2b$12$JK7GjnX7eDjsKPVAcCN77.LGEzg6x1YZfXW.FjkitbbZZ48FUHiG.', 'Brayan Josser', 'Fernandez Ebrath', '5678901234'),
    ('1239', 'earrieta@unibarranquilla.edu.co', '$2b$12$J6UTbnxQw3Hrqvc9e6g9w.HicGQwWAL8YJlaQIQr4Y3ArkftTdBsC', 'Evelio Ramiro', 'Arrieta Torres', '6789012345'),
    ('1240', 'rvaliente@unibarranquilla.edu.co', '$2b$12$AZWh6CVt0nS92u2OByFG7emf/R5mh1b/1/QUF8kt/VS3OscqY6wHm', 'Ricardo Josue', 'Valiente Ortiz', '1111111111'),
    ('1241', 'jmcerro@unibarranquilla.edu.co', '$2b$12$xysXIB9Dv96o3btGMuJGnu2YTVFyFPWehoXZ3TtLON1hYiwR1fzTy', 'Jose Manuel', 'Cerro Acuña', '2222222222'),
    ('1242', 'dalbertovasquez@unibarranquilla.edu.co', '$2b$12$rnpIaLOsY6ZYRFkpmvFiJ.hGPTZPW7qd0oQZA0lqZoNEShqdrlR4S', 'Diego Alberto', 'Vasquez Arteaga', '7890123456'),
    ('1243', 'djosecarrillo@unibarranquilla.edu.co', '$2b$12$wrMniy6v482eJV.SdEDmJet6CALs6.IWtcjmhSJ5u/cKhwsnKW3e2', 'David Jose', 'Carrillo Quevedo', '8901234567');

INSERT INTO usuarios_roles (id_usuario, id_rol)
VALUES
    ('1237', 1),
    ('1237', 3),
    ('1234', 3),
    ('1235', 3),
    ('1236', 3),
    ('1238', 2),
    ('1239', 2),
    ('1240', 3),
    ('1241', 3),
    ('1242', 3),
    ('1243', 3);

INSERT INTO profesor (id_profesor) 
VALUES
    ('1238'),
    ('1239');

INSERT INTO modulos (id_modulo, nombre, creditos)
VALUES
    ('COM35', 'Paginas web', 2),
    ('IMD02', 'Proyecto integrador', 1),
    ('COM22', 'Produccion multimedial', 1),
    ('COM26', 'Bases de datos', 3),
    ('COM25', 'Estructuras de datos', 3);

INSERT INTO salones (sede, nombre)
VALUES
    ('barranquilla', 'salon 01'),
    ('barranquilla', 'salon 02'),
    ('barranquilla', 'salon 03'),
    ('barranquilla', 'salon 04'),
    ('soledad', 'salon B4-1'),
    ('soledad', 'salon C1-2'),
    ('soledad', 'salon D3-3'),
    ('soledad', 'salon E2-4');

INSERT INTO grupo (id_grupo, id_modulo, id_profesor, id_salon, periodo, dia_semana, hora_inicio, hora_fin)
VALUES
    ('SIN_G1', 'COM35', '1238', 1, '2024-2', 'lunes', '07:00:00', '09:00:00'), 
    ('SIN_G2', 'IMD02', '1238', 2, '2024-2', 'martes', '08:00:00', '10:00:00'),
    ('SIN_G3', 'COM22', '1238', 3, '2024-2', 'miércoles', '09:00:00', '11:00:00'),
    ('SIN_G4', 'COM26', '1239', 4, '2024-2', 'jueves', '10:00:00', '12:00:00'),  
    ('SIN_G5', 'COM25', '1239', 5, '2024-2', 'viernes', '11:00:00', '13:00:00'),
    ('SIN_G6', 'IMD02', '1239', 6, '2024-2', 'sábado', '12:00:00', '14:00:00');

INSERT INTO estudiante (id_estudiante, id_programa)
VALUES
    ('1234', 1),
    ('1235', 1),
    ('1236', 1),
    ('1237', 1),
    ('1240', 1),
    ('1241', 1),
    ('1242', 1),
    ('1243', 1);

INSERT INTO matricula (id_grupo, id_modulo, id_estudiante, periodo)
VALUES
    ('SIN_G1', 'COM35', '1234', '2024-2'),
    ('SIN_G2', 'IMD02', '1234', '2024-2'),
    ('SIN_G3', 'COM22', '1234', '2024-2'),
    ('SIN_G4', 'COM26', '1234', '2024-2'),
    ('SIN_G1', 'COM35', '1235', '2024-2'),
    ('SIN_G2', 'IMD02', '1235', '2024-2'),
    ('SIN_G3', 'COM22', '1235', '2024-2'),
    ('SIN_G4', 'COM26', '1235', '2024-2'),
    ('SIN_G1', 'COM35', '1236', '2024-2'),
    ('SIN_G2', 'IMD02', '1236', '2024-2'),
    ('SIN_G3', 'COM22', '1236', '2024-2'),
    ('SIN_G4', 'COM26', '1236', '2024-2'),
    ('SIN_G1', 'COM35', '1237', '2024-2'),
    ('SIN_G2', 'IMD02', '1237', '2024-2'),
    ('SIN_G3', 'COM22', '1237', '2024-2'),
    ('SIN_G4', 'COM26', '1237', '2024-2'),
    ('SIN_G4', 'COM26', '1240', '2024-2'),
    ('SIN_G5', 'COM25', '1240', '2024-2'),
    ('SIN_G6', 'IMD02', '1240', '2024-2'),
    ('SIN_G1', 'COM35', '1241', '2024-2'),
    ('SIN_G2', 'IMD02', '1241', '2024-2'),
    ('SIN_G3', 'COM22', '1241', '2024-2'),
    ('SIN_G5', 'COM25', '1241', '2024-2'),
    ('SIN_G1', 'COM35', '1242', '2024-2'),
    ('SIN_G3', 'COM22', '1242', '2024-2'),
    ('SIN_G4', 'COM26', '1242', '2024-2'),
    ('SIN_G6', 'IMD02', '1242', '2024-2'),
    ('SIN_G2', 'IMD02', '1243', '2024-2'),
    ('SIN_G3', 'COM22', '1243', '2024-2'),
    ('SIN_G5', 'COM25', '1243', '2024-2'),
    ('SIN_G6', 'IMD02', '1243', '2024-2');

INSERT INTO asistencias (id_estudiante, id_grupo, id_modulo, periodo, fecha, hora_llegada)
VALUES
    ('1234', 'SIN_G1', 'COM35', '2024-2', '2024-07-15', '07:05:00'), -- lunes
    ('1234', 'SIN_G2', 'IMD02', '2024-2', '2024-07-16', '08:03:00'), -- martes
    ('1234', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'), -- miércoles
    ('1234', 'SIN_G4', 'COM26', '2024-2', '2024-07-18', '10:10:00'), -- jueves
    ('1234', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'), -- viernes
    ('1234', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00'), -- sábado
    ('1235', 'SIN_G1', 'COM35', '2024-2', '2024-07-15', '07:05:00'),
    ('1235', 'SIN_G2', 'IMD02', '2024-2', '2024-07-16', '08:03:00'),
    ('1235', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'),
    ('1235', 'SIN_G4', 'COM26', '2024-2', '2024-07-18', '10:10:00'),
    ('1235', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'),
    ('1235', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00'),
    ('1236', 'SIN_G1', 'COM35', '2024-2', '2024-07-15', '07:05:00'),
    ('1236', 'SIN_G2', 'IMD02', '2024-2', '2024-07-16', '08:03:00'),
    ('1236', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'),
    ('1236', 'SIN_G4', 'COM26', '2024-2', '2024-07-18', '10:10:00'),
    ('1236', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'),
    ('1236', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00'),
    ('1237', 'SIN_G1', 'COM35', '2024-2', '2024-07-15', '07:05:00'),
    ('1237', 'SIN_G2', 'IMD02', '2024-2', '2024-07-16', '08:03:00'),
    ('1237', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'),
    ('1237', 'SIN_G4', 'COM26', '2024-2', '2024-07-18', '10:10:00'),
    ('1237', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'),
    ('1237', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00'),
    ('1240', 'SIN_G4', 'COM26', '2024-2', '2024-07-18', '10:10:00'),
    ('1240', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'),
    ('1240', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00'),
    ('1241', 'SIN_G1', 'COM35', '2024-2', '2024-07-15', '07:05:00'),
    ('1241', 'SIN_G2', 'IMD02', '2024-2', '2024-07-16', '08:03:00'),
    ('1241', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'),
    ('1241', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'),
    ('1242', 'SIN_G1', 'COM35', '2024-2', '2024-07-15', '07:05:00'),
    ('1242', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'),
    ('1242', 'SIN_G4', 'COM26', '2024-2', '2024-07-18', '10:10:00'),
    ('1242', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00'),
    ('1243', 'SIN_G2', 'IMD02', '2024-2', '2024-07-16', '08:03:00'),
    ('1243', 'SIN_G3', 'COM22', '2024-2', '2024-07-17', '09:07:00'),
    ('1243', 'SIN_G5', 'COM25', '2024-2', '2024-07-19', '11:12:00'),
    ('1243', 'SIN_G6', 'IMD02', '2024-2', '2024-07-20', '12:15:00');
